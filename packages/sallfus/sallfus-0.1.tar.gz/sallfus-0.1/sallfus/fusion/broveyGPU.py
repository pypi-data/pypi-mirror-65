# -*- coding: utf-8 -*-
import skimage.io
import pycuda.autoinit
import pycuda.driver as drv
import pycuda.gpuarray as gpuarray
import numpy as np
import skcuda.linalg as linalg
from pycuda.elementwise import ElementwiseKernel
import sys
import time


# El step_1 realiza la la divisiÃ³n de la banda entre la suma de las bandas
def step_1(matrix_color, matrix_suma):
    #La funciÃ³n gpuarray.if_positive evalua cada posiciÃ³n de la matriz
    #Y de acuerdo a su valor realiza la primer operaciÃ³n o la segunda constatando una sentencia If Else
    matrix_1 = gpuarray.if_positive(matrix_suma,(3*matrix_color)/matrix_suma,matrix_suma)
    return matrix_1

# El step_2 realiza la multiplicaciÃ³n posiciÃ³n a posiciÃ³n del step_1 por la pancromatica
def step_2(matrix_1, matrix_image_pan):
    #La funciÃ³n linalg.mulitply realiza la multiplicaciÃ³n elemento a elemento entre dos matrices
    matrix_2 = linalg.multiply(matrix_1, matrix_image_pan)
    return matrix_2

# El step_3 determina el valor maximo y minimo de la banda resultante de la transformada de brovey
def step_3(matrix_1):
    #La funciÃ³n np.max determina el maximo valor de un array
    #La funciÃ³n np.min determina el minimo valor de un array
    mat_max = np.amax(matrix_1.get())
    mat_min = np.amin(matrix_1.get())
    return mat_max, mat_min

# El step_4 realiza un ajuste de riqueza espectral llamado rescale global min
def step_4(matrix_1, matrix_color, mat_max, mat_min):
    #La funciÃ³n lin_comb invoca el kernel elementwise establecido para llevar a cabo el ajuste por rescale global min
    lin_comb(mat_min, matrix_1, mat_max, matrix_color)
    return matrix_color

# Kernel establecido para llevar a cabo el mÃ©todo de rescale global min
lin_comb = ElementwiseKernel(
        "float a, float *x, float b, float *z",
        "z[i] = ((x[i]-a)*255)/(b-a)",
        "linear_combination")

def fusion_images(multispectral, panchromatic, save_image=False, savepath=None, timeCondition=True):
    #Verifica que ambas imagenes cumplan con las condiciones
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

    # Convierte a float32 y separa las bandas RGB de la multispectral
    multispectral = multispectral.astype(np.float32)
    r = multispectral[:,:,0].astype(np.float32)
    g = multispectral[:,:,1].astype(np.float32)
    b = multispectral[:,:,2].astype(np.float32)
    b = b.astype(np.float32)
    # Convierte la pancromatica a float32
    panchromatic = panchromatic.astype(np.float32)
    # Suma las bandas de la multispectral
    msuma = r+g+b
    start=time.time()
    r_gpu = gpuarray.to_gpu(r)
    g_gpu = gpuarray.to_gpu(g)
    b_gpu = gpuarray.to_gpu(b)
    panchromatic_gpu = gpuarray.to_gpu(panchromatic)
    msuma_gpu = gpuarray.to_gpu(msuma)

    linalg.init()
    m11_gpu = step_1(r_gpu, msuma_gpu)
    m22_gpu = step_2(m11_gpu, panchromatic_gpu)

    m33_gpu = step_1(b_gpu, msuma_gpu)
    m44_gpu = step_2(m33_gpu, panchromatic_gpu)

    m55_gpu = step_1(g_gpu, msuma_gpu)
    m66_gpu = step_2(m55_gpu, panchromatic_gpu)

    Amax_host, Amin_host = step_3(m22_gpu)
    rr_gpu = gpuarray.empty_like(r_gpu)
    step_4(m22_gpu, rr_gpu, Amax_host, Amin_host)

    Amax_host, Amin_host = step_3(m66_gpu)
    gg_gpu = gpuarray.empty_like(g_gpu)
    step_4(m66_gpu, gg_gpu, Amax_host, Amin_host)

    Amax_host, Amin_host = step_3(m44_gpu)
    bb_gpu = gpuarray.empty_like(b_gpu)
    step_4(m44_gpu, bb_gpu, Amax_host, Amin_host)
    end = time.time()

    ggg_host = gg_gpu.get().astype(np.uint8)
    rrr_host = rr_gpu.get().astype(np.uint8)
    bbb_host = bb_gpu.get().astype(np.uint8)

    # Combina las bandas resultantes
    fusioned_image = np.stack((rrr_host, ggg_host, bbb_host),axis=2)
    if(save_image):
        # Guarda la imagen resultando de acuerdo al tercer parametro establecido en la linea de ejecución del script
        if(savepath != None):
            t = skimage.io.imsave(savepath+'/broveygpu_image.tif',fusioned_image, plugin='tifffile')
        else:
            t = skimage.io.imsave('broveygpu_image.tif',fusioned_image, plugin='tifffile')
    #time_calculated de ejecución para la transformada de Brovey en GPU
    time_calculated = (end-start)
    if(timeCondition):
        return {"image": fusioned_image, "time" :  time_calculated}
    else:
        return fusioned_image
