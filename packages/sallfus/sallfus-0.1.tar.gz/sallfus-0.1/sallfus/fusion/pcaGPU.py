# -*- coding: utf-8 -*-
import skimage.io
import numpy as np
from numpy import linalg as la
import cv2
import pycuda.autoinit
import pycuda.driver as drv
import pycuda.gpuarray as gpuarray
from pycuda import compiler
import numpy as np
import skcuda.linalg as linalg
import skcuda.misc as misc
from pycuda.elementwise import ElementwiseKernel
import pycuda.cumath as cumath
import sys, getopt
import time


BLOCK_SIZE = 32
# Kernel template para llevar a cabo el calculo de la matriz de varianza-covarianza
kernel_var_cov = """
#include <stdio.h>
__global__ void CovarianceKernel(float *R, float *G, float *B,float *D)
{
    // Thread index
    const uint tx = threadIdx.x;
    const uint ty = threadIdx.y;
    __shared__ float prueba_salida;
    if (threadIdx.x == 0) prueba_salida = 0;
    float valor_temp = 0;
    float salida_temp[9];
    __syncthreads();

    const int size = 3;
    float arreglo[size];

    arreglo[0] = R[ty * %(BLOCK_SIZE)s + tx];
    arreglo[1] = G[ty * %(BLOCK_SIZE)s + tx];
    arreglo[2] = B[ty * %(BLOCK_SIZE)s + tx];
    __syncthreads();

    for(int k = 0; k < 3; k++){
        for(int h = 0; h < 3; h++){
            valor_temp = arreglo[k]*arreglo[h];
            salida_temp[k*3+h] = valor_temp;
            valor_temp = 0;
        }
    }
    __syncthreads();

   for (int i = 0; i < 9; ++i){
    atomicAdd(&prueba_salida,salida_temp[i]);
    __syncthreads();
    D[i] += prueba_salida;
    __syncthreads();
    prueba_salida = 0.0;
    __syncthreads();
   }

}
"""
# Kernel template para llevar a cabo el calculo de componente principales originales
kernel_componentes_principales_original = """
#include <stdio.h>
__global__ void componentesPrincipalesOriginal(float *R, float *G, float *B, float *Q, float *S1, float *S2, float *S3)
{
    // Thread index
    const uint tx = threadIdx.x;
    const uint ty = threadIdx.y;


    const int size = 3;
    float salida_temp [size];
    float valor_temp = 0.0;
    float arreglo[size];
    //__syncthreads();




    arreglo[0] = R[ty * %(BLOCK_SIZE)s + tx];
    arreglo[1] = G[ty * %(BLOCK_SIZE)s + tx];
    arreglo[2] = B[ty * %(BLOCK_SIZE)s + tx];
    __syncthreads();



    for(int i = 0; i < 3; ++i){
        for(int j = 0; j < 3; ++j){
            valor_temp += (Q[i*3+j] * arreglo[j]);
        }
        salida_temp[i] = valor_temp;
        valor_temp = 0.0;
    }
    __syncthreads();

    S1[ty * %(BLOCK_SIZE)s + tx] = salida_temp[0];
    __syncthreads();
    S2[ty * %(BLOCK_SIZE)s + tx] = (-1.0)*salida_temp[1];
    __syncthreads();
    S3[ty * %(BLOCK_SIZE)s + tx] = salida_temp[2];
    __syncthreads();

}
"""

# Kernel template para llevar a cabo el calculo de componente principales con la pancromática
kernel_componentes_principales_pancromatica = """
#include <stdio.h>
__global__ void componentesPrincipalesPancromatica(float *R, float *G, float *B, float *E, float *S1, float *S2, float *S3)
{
    // Thread index
    const uint tx = threadIdx.x;
    const uint ty = threadIdx.y;


    const int size = 3;
    float salida_temp [size];
    float valor_temp = 0.0;
    float arreglo[size];





    arreglo[0] = R[ty * %(BLOCK_SIZE)s + tx];
    arreglo[1] = G[ty * %(BLOCK_SIZE)s + tx];
    arreglo[2] = B[ty * %(BLOCK_SIZE)s + tx];
    __syncthreads();



    for(int i = 0; i < 3; ++i){
        for(int j = 0; j < 3; ++j){
            valor_temp += (E[i*3+j] * arreglo[j]);
        }
        salida_temp[i] = valor_temp;
        valor_temp = 0.0;
    }
    __syncthreads();

    S1[ty * %(BLOCK_SIZE)s + tx] = salida_temp[0];
    __syncthreads();
    S2[ty * %(BLOCK_SIZE)s + tx] = salida_temp[1];
    __syncthreads();
    S3[ty * %(BLOCK_SIZE)s + tx] = salida_temp[2];
    __syncthreads();

}
"""

# Función para dividir una matriz en un submatrices cuadradas
def split(array, nrows, ncols):
    """Split a matrix into sub-matrices."""
    r, h = array.shape
    return (array.reshape(h//nrows, nrows, -1, ncols)
                 .swapaxes(1, 2)
                 .reshape(-1, nrows, ncols))

# Funcion para calcular la matriz de varianza-covarianza
def varianza_cov( R_s, G_s, B_s):
    kernel_code = kernel_var_cov % {
        'BLOCK_SIZE': BLOCK_SIZE
        }
    mod = compiler.SourceModule(kernel_code)
    covariance_kernel = mod.get_function("CovarianceKernel")
    salida_gpu = gpuarray.zeros((3, 3), np.float32)
    Rs_gpu = gpuarray.to_gpu(R_s)
    Gs_gpu = gpuarray.to_gpu(G_s)
    Bs_gpu = gpuarray.to_gpu(B_s)
    for i in range(len(R_s)):
        covariance_kernel(
            # inputs
            Rs_gpu[i], Gs_gpu[i], Bs_gpu[i],
            # output
            salida_gpu,
            # block of multiple threads
            block = (32, 32, 1),
            )
    return salida_gpu.get()

# Función para realizar el Stack de las submatrices resultantes de alguna rutina realizada
def stack_values(list_cp, array_split, size, block_size):
    block_size = block_size
    valor_inicial = 0
    valor_final = 0
    list_cp_nueva = []
    factor_div = (size//block_size)
    factor_ite = len(array_split)//factor_div
    for i in range(factor_ite):
        valor_final = valor_final + factor_div
        list_cp_nueva.append(np.hstack(list_cp[valor_inicial:valor_final]))
        valor_inicial = valor_inicial + factor_div
    cp_final = np.vstack(list_cp_nueva)
    return cp_final

# Funcion para calcular los componentes principales originales
def componentes_principales_original(r_s , g_s, b_s, q, size, block_size):
    cp1_temp = []
    cp2_temp = []
    cp3_temp = []
    size = size
    block_size = block_size
    kernel_code = kernel_componentes_principales_original % {
        'BLOCK_SIZE': BLOCK_SIZE,
        }
    mod = compiler.SourceModule(kernel_code)
    kernel = mod.get_function("componentesPrincipalesOriginal")
    s1_gpu = gpuarray.zeros((block_size,block_size),np.float32)
    s2_gpu = gpuarray.zeros((block_size,block_size),np.float32)
    s3_gpu = gpuarray.zeros((block_size,block_size),np.float32)
    q_gpu = gpuarray.to_gpu(q)
    Rs_gpu_t = gpuarray.to_gpu(r_s)
    Gs_gpu_t = gpuarray.to_gpu(g_s)
    Bs_gpu_t = gpuarray.to_gpu(b_s)
    for i in range(len(r_s)):
        kernel(
            # inputs
            Rs_gpu_t[i], Gs_gpu_t[i], Bs_gpu_t[i], q_gpu,
            # output
            s1_gpu, s2_gpu, s3_gpu,
            # block of multiple threads
            block = (block_size, block_size, 1),
            )
        cp1_temp.append(s1_gpu.get())
        cp2_temp.append(s2_gpu.get())
        cp3_temp.append(s3_gpu.get())
    cp1 = stack_values(cp1_temp, r_s, size, block_size)
    cp2 = stack_values(cp2_temp, r_s, size, block_size)
    cp3 = stack_values(cp3_temp, r_s, size, block_size)
    return cp1, cp2, cp3

# Funcion para calcular los componentes principales mediante la pancromática
def componentes_principales_panchromartic(r_s , g_s, b_s, q, size, block_size):
    block_size = block_size
    nb1_temp = []
    nb2_temp = []
    nb3_temp = []
    size = size
    kernel_code = kernel_componentes_principales_pancromatica % {
        'BLOCK_SIZE': BLOCK_SIZE,
        }
    mod = compiler.SourceModule(kernel_code)
    kernel = mod.get_function("componentesPrincipalesPancromatica")
    s1_gpu = gpuarray.zeros((block_size,block_size),np.float32)
    s2_gpu = gpuarray.zeros((block_size,block_size),np.float32)
    s3_gpu = gpuarray.zeros((block_size,block_size),np.float32)
    Rs_gpu_t = gpuarray.to_gpu(r_s)
    Gs_gpu_t = gpuarray.to_gpu(g_s)
    Bs_gpu_t = gpuarray.to_gpu(b_s)
    q_gpu = gpuarray.to_gpu(q)
    for i in range(len(r_s)):
        kernel(
            # inputs
            Rs_gpu_t[i], Gs_gpu_t[i], Bs_gpu_t[i], q_gpu,
            # output
            s1_gpu, s2_gpu, s3_gpu,
            # block of multiple threads
            block = (block_size, block_size, 1),
            )
        nb1_temp.append(s1_gpu.get())
        nb2_temp.append(s2_gpu.get())
        nb3_temp.append(s3_gpu.get())
    nb1 = stack_values(nb1_temp, g_s, size, block_size)
    nb2 = stack_values(nb2_temp, g_s, size, block_size)
    nb3 = stack_values(nb3_temp, g_s, size, block_size)
    return nb1, nb2, nb3



# Kernel establecido para llevar a cabo la resta de las medias de cada banda a cada pixel de una banda
substract = ElementwiseKernel(
        "float *x, float y, float *z",
        "z[i] = x[i]-y",
        "substract_value")

# Kernel establecido para realiza un ajuste cuando el valor de un pixel es menor a 0
negative_adjustment = ElementwiseKernel(
        "float *x, float *z",
        "if(x[i] < 0){z[i] = 0.0;}else{z[i] = x[i];}",
        "adjust_value")


# Funcion encargada de realizar las potencias sucesivas
def successive_powers(ortogonal_matrix):
    size_mat_ort = len(ortogonal_matrix)
    s = np.zeros((size_mat_ort,1))
    B = np.zeros((size_mat_ort,size_mat_ort))
    for i in range(1, (size_mat_ort+1)):
        B=la.matrix_power(ortogonal_matrix,i)
        s[i-1]=np.trace(B)
    return s

# Esta funcion tiene como objetivo calcular los coeficientes del polinomio caracteristico
def polynomial_coefficients(polynomial_trace, ortogonal_matrix):
    n_interations = len(ortogonal_matrix)
    polynomial = np.zeros((n_interations))
    polynomial[0] = -polynomial_trace[0]
    for i in range(1,n_interations):
        polynomial[i]=-polynomial_trace[i]/(i+1)
        for j in range(i):
            polynomial[i]=polynomial[i]-(polynomial[j]*(polynomial_trace[(i-j)-1])/(i+1))
    return polynomial

# Funcion para calcular los vectores propios normalizados
def eigenvectors_norm(mat_eigenvalues, ortogonal_matrix, mat_eigenvectors):
    n = len(mat_eigenvalues)
    V = np.zeros((n,n))
    S = np.zeros((n,1))
    for i in range(n):
        B= ortogonal_matrix[1:n,1:n]-mat_eigenvalues[i,i]*np.eye(n-1)
        temp_s=la.lstsq(B,mat_eigenvectors,rcond=-1)[0].transpose()
        S=np.insert(temp_s,0,1);
        V[0:n,i]=S/la.norm(S)
    return V, V.transpose()

def fusion_images(multispectral, panchromatic, save_image=False, savepath=None, timeCondition=True):
    end = 0
    start = 0

    #Verifica que ambas imagenes cumplan con las condiciones
    if multispectral.shape[2] == 3:
        print('The Multispectral image has '+str(multispectral.shape[2])+' channels and size of '+str(multispectral.shape[0])+'x'+str(multispectral.shape[1]))
    else:
        sys.exit('The first image is not multispectral')

    if len(panchromatic.shape) == 2:
        print(' The Panchromatic image has a size of '+str(panchromatic.shape[0])+'x'+str(panchromatic.shape[1]))
    else:
        sys.exit('The second image is not panchromatic')

    size_rgb = multispectral.shape

    # Definición del tamaño del bloque
    BLOCK_SIZE = 32


    # Convierte a float32 y separa las bandas RGB de la multispectral
    m_host = multispectral.astype(np.float32)
    r_host = m_host[:,:,0].astype(np.float32)
    g_host = m_host[:,:,1].astype(np.float32)
    b_host = m_host[:,:,2].astype(np.float32)
    size_rgb = multispectral.shape
    # Convierte la pancromatica a float32
    panchromatic_host = panchromatic.astype(np.float32)


    # Inicial el time_calculated de ejecucion
    start=time.time()

    # Se pasan los array en el host al device
    r_gpu = gpuarray.to_gpu(r_host)
    g_gpu = gpuarray.to_gpu(g_host)
    b_gpu = gpuarray.to_gpu(b_host)
    p_gpu = gpuarray.to_gpu(panchromatic_host)

    # Se calcula la media de cada una de las bandas y se forma un arreglo con estos valores, todo esto en GPU
    mean_r_gpu = misc.mean(r_gpu)
    mean_g_gpu = misc.mean(g_gpu)
    mean_b_gpu = misc.mean(b_gpu)

    # Se obtiene el numero de bandas
    n_bands = size_rgb[2]

    # Se aparta memoria en GPU
    r_gpu_subs = gpuarray.zeros_like(r_gpu,np.float32)
    g_gpu_subs = gpuarray.zeros_like(g_gpu,np.float32)
    b_gpu_subs = gpuarray.zeros_like(b_gpu,np.float32)

    # Se realiza la resta de su respectiva media a cada uno de los pixeles de cada banda,
    substract( r_gpu, mean_r_gpu.get(), r_gpu_subs)
    substract( g_gpu, mean_g_gpu.get(), g_gpu_subs)
    substract( b_gpu, mean_b_gpu.get(), b_gpu_subs)

    # Se divide cada una de las bandas después de ser restada su media, en un conjunto de submatrices cuadradas del tamaño del bloque
    r_subs_split = split(r_gpu_subs.get(),BLOCK_SIZE,BLOCK_SIZE)
    g_subs_split = split(g_gpu_subs.get(),BLOCK_SIZE,BLOCK_SIZE)
    b_subs_split = split(b_gpu_subs.get(),BLOCK_SIZE,BLOCK_SIZE)

    #Se obtiene la matrix de varianza y covarianza
    mat_var_cov = varianza_cov(r_subs_split,g_subs_split,b_subs_split)

    # Coeficiente para diaganalizar ortogonalmente
    coefficient = 1.0/((size_rgb[0]*size_rgb[1])-1)

    # Matriz diagonalizada ortogonalmente
    ortogonal_matrix = mat_var_cov*coefficient

    # Se calcula la traza de las sucesivas potencias de la matriz ortogonal inicial
    polynomial_trace = successive_powers(ortogonal_matrix)


    # Se calculan los coeficientes del polinomio caracteristico
    characteristic_polynomial = polynomial_coefficients(polynomial_trace, ortogonal_matrix)

    # Se obtienen las raices del polinomio caracteristico
    characteristic_polynomial_roots = np.roots(np.insert(characteristic_polynomial,0,1))


    # Los vectores propios aparecen en la diagonal de la matriz eigenvalues_mat
    eigenvalues_mat = np.diag(characteristic_polynomial_roots)


    # Vectores propios para cada valor propio
    eigenvectors_mat = -1*ortogonal_matrix[1:n_bands,0]

    # Se calcular los vectores propios normalizados
    # Cada vector propio es una columna de la matriz mat_ortogonal_base
    mat_ortogonal_base, q_matrix = eigenvectors_norm(eigenvalues_mat, ortogonal_matrix, eigenvectors_mat)
    q_matrix_list = q_matrix.tolist()
    q_matrix_cpu = np.array(q_matrix_list).astype(np.float32)
    w1 = q_matrix_cpu[0,:]
    w2 = (-1)*q_matrix_cpu[1,:]
    w3 = q_matrix_cpu[2,:]
    eigenvectors = np.array((w1,w2,w3))

    # Se calcula la inversa de los vectores propios
    inv_eigenvectors = la.inv(eigenvectors)
    inv_list = inv_eigenvectors.tolist()
    inv_eigenvector_cpu = np.array(inv_list).astype(np.float32)

    # Se realiza la división de las bandas en submatrices del tamaño del bloque
    r_subs_split_cp = split(r_host,BLOCK_SIZE,BLOCK_SIZE)
    g_subs_split_cp = split(g_host,BLOCK_SIZE,BLOCK_SIZE)
    b_subs_split_cp = split(b_host,BLOCK_SIZE,BLOCK_SIZE)

    # Se calculan los componentes principales con las bandas originales y los vectores propios
    pc_1,pc_2,pc_3 = componentes_principales_original(r_subs_split_cp,g_subs_split_cp,b_subs_split_cp,q_matrix_cpu,r_host.shape[0], BLOCK_SIZE)

    # Se realiza la división en submatrices de la pancromática, el componente principal 2 y 3, del tamaño del bloque,
    p_subs_split_nb = split(panchromatic_host,BLOCK_SIZE,BLOCK_SIZE)
    pc_2_subs_split_nb = split(pc_2,BLOCK_SIZE,BLOCK_SIZE)
    pc_3_subs_split_nb = split(pc_3,BLOCK_SIZE,BLOCK_SIZE)

    # Se calculan los componentes con la pancromatica, componentes principales originales 2 y 3, y la inversa de los vectores propios
    nb1,nb2,nb3 = componentes_principales_panchromartic(p_subs_split_nb,pc_2_subs_split_nb,pc_3_subs_split_nb,inv_eigenvector_cpu,r_host.shape[0], BLOCK_SIZE)

    nb11 = nb1.astype(np.float32)
    nb22 = nb2.astype(np.float32)
    nb33 = nb3.astype(np.float32)


    nb11_gpu = gpuarray.to_gpu(nb11)
    nb22_gpu = gpuarray.to_gpu(nb22)
    nb33_gpu = gpuarray.to_gpu(nb33)

    # Se separa espacio en memoria para las matrices resultado de realizar el ajuste
    nb111_gpu = gpuarray.empty_like(nb11_gpu)
    nb222_gpu = gpuarray.empty_like(nb22_gpu)
    nb333_gpu = gpuarray.empty_like(nb33_gpu)

    # Se realiza un ajuste cuando los valores de cada pixel es menor a 0, en GPU
    negative_adjustment(nb11_gpu,nb111_gpu)
    negative_adjustment(nb22_gpu,nb222_gpu)
    negative_adjustment(nb33_gpu,nb333_gpu)

    nb111_cpu = nb111_gpu.get().astype(np.uint8)
    nb222_cpu = nb222_gpu.get().astype(np.uint8)
    nb333_cpu = nb333_gpu.get().astype(np.uint8)


    end = time.time()


    fusioned_image=np.stack((nb111_cpu,nb222_cpu,nb333_cpu),axis=2);
    if(save_image):
        # Guarda la imagen resultando de acuerdo al tercer parametro establecido en la linea de ejecución del script
        if(savepath != None):
            t = skimage.io.imsave(savepath+'/pcagpu_image.tif',fusioned_image, plugin='tifffile')
        else:
            t = skimage.io.imsave('pcagpu_image.tif',fusioned_image, plugin='tifffile')
    #time_calculated de ejecución para la transformada de Brovey en GPU
    time_calculated = (end-start)
    if(timeCondition):
        return {"image": fusioned_image, "time" :  time_calculated}
    else:
        return fusioned_image
