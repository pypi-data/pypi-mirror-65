# -*- coding: utf-8 -*-
import numpy as np
from numpy import linalg as la
import skimage.io
import numpy as np
import sys
import time

# Funcion para calcular la matriz de varianza-covarianza
def varianza_cov(r_band,g_band, b_band, mat_means, size):
    var_cov_mat = np.zeros((size,size))
    for i in range(r_band.shape[0]):
        for j in range(r_band.shape[1]):
            temp_a = np.array([[r_band[i][j]],[g_band[i][j]],[b_band[i][j]]]-mat_means)
            temp_b = temp_a.transpose()
            mul_temps = np.multiply(temp_a,temp_b)
            var_cov_mat= var_cov_mat+mul_temps
    return var_cov_mat

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

# Funcion para calcular los componentes principales originales
def componentes_principales_original(r_band, g_band, b_band, mat_q):
    acp = np.zeros((r_band.shape[0],r_band.shape[1]))
    cp1 = np.zeros((r_band.shape[0],r_band.shape[1]))
    cp2 = np.zeros((g_band.shape[0],g_band.shape[1]))
    cp3 = np.zeros((b_band.shape[0],b_band.shape[1]))
    for i in range(r_band.shape[0]):
        for j in range(r_band.shape[1]):
            acp = np.dot(mat_q,np.array(([r_band[i,j]],[g_band[i,j]],[b_band[i,j]])))
            cp1[i,j] = acp[0,0]
            cp2[i,j] = acp[1,0]
            cp3[i,j] = acp[2,0]
    cp2 = (-1)*cp2
    return cp1, cp2, cp3

# Funcion para calcular los componentes principales mediante la pancromatica
def componentes_principales_panchromartic(panchromatic, cp_2, cp_3, inv_eigenvector):
    nb1 = np.zeros((cp_2.shape[0],cp_2.shape[1]))
    nb2 = np.zeros((cp_2.shape[0],cp_2.shape[1]))
    nb3 = np.zeros((cp_2.shape[0],cp_2.shape[1]))
    for i in range(cp_2.shape[0]):
        for j in range(cp_2.shape[1]):
            iacp = np.dot(inv_eigenvector,np.array(([panchromatic[i,j]],[cp_2[i,j]],[cp_3[i,j]])))
            nb1[i,j] = iacp[0,0]
            nb2[i,j] = iacp[1,0]
            nb3[i,j] = iacp[2,0]
    return nb1, nb2, nb3

# Funcion que realiza un ajuste cuando el valor de un pixel es menor a 0
def negative_adjustment(band):
    for i in range(band.shape[0]):
        for j in range(band.shape[1]):
            if band[i,j] < 0:
                band[i,j] = 0.0
    return band

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


    # Convierte a float32 y separa las bandas RGB de la multispectral
    mmultispectral = multispectral.astype(np.float32)
    r = multispectral[:,:,0].astype(np.float32)
    g = multispectral[:,:,1].astype(np.float32)
    b = multispectral[:,:,2].astype(np.float32)
    # Convierte la pancromatica a float32
    panchromatic = panchromatic.astype(np.float32)


    # Inicial el time_calculated de ejecucion
    start=time.time()

    # Se calcula la media de cada una de las bandas y se forma un arreglo con estos valores
    m1 = np.mean(r)
    m2 = np.mean(g)
    m3 = np.mean(b)
    m_means = np.array([[m1],[m2],[m3]])

    # Se obtiene el numero de bandas
    n_bands = size_rgb[2]

    #Se obtiene la matrix de varianza y covarianza
    mat_var_cov = varianza_cov(r,g,b,m_means,n_bands)

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
    #Cada vector propio es una columna de la matriz mat_ortogonal_base
    mat_ortogonal_base, q_matrix = eigenvectors_norm(eigenvalues_mat, ortogonal_matrix, eigenvectors_mat)
    w1 = q_matrix[0,:]
    w2 = (-1)*q_matrix[1,:]
    w3 = q_matrix[2,:]
    eigenvectors = np.array((w1,w2,w3))

    # Se calcula la inversa de los vectores propios
    inv_eigenvectors = la.inv(eigenvectors)

    # Se calculan los componentes principales con las bandas originales y los vectores propios
    pc_1, pc_2, pc_3 = componentes_principales_original(r,g,b,q_matrix)

    # Se calculan los componentes con la pancromatica, componentes principales originales 2 y 3, y la inversa de los vectores propios
    nb_1, nb_2, nb_3 = componentes_principales_panchromartic(panchromatic, pc_2, pc_3, inv_eigenvectors)

    nb11 = nb_1.astype(np.float32)
    nb22 = nb_2.astype(np.float32)
    nb33 = nb_3.astype(np.float32)

    # Se realiza un ajuste cuando los valores de cada pixel es menor a 0
    nb11 = negative_adjustment(nb11)
    nb22 = negative_adjustment(nb22)
    nb33 = negative_adjustment(nb33)


    nb111 = nb11.astype(np.uint8)
    nb222 = nb22.astype(np.uint8)
    nb333 = nb33.astype(np.uint8)

    end = time.time()

    # Se realiza un stack con los componentes resultantes
    fusioned_image = np.stack((nb111,nb222,nb333),axis=2)
    if(save_image):
        # Guarda la imagen resultando de acuerdo al tercer parametro establecido en la linea de ejecución del script
        if(savepath != None):
            t = skimage.io.imsave(savepath+'/pcacpu_image.tif',fusioned_image, plugin='tifffile')
        else:
            t = skimage.io.imsave('pcacpu_image.tif',fusioned_image, plugin='tifffile')
    #time_calculated de ejecución para la transformada de Brovey en GPU
    time_calculated = (end-start)
    if(timeCondition):
        return {"image": fusioned_image, "time" :  time_calculated}
    else:
        return fusioned_image
