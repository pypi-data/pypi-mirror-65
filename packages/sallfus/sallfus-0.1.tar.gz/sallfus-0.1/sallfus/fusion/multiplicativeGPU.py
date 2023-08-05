# -*- coding: utf-8 -*-
import skimage.io
import numpy as np
import pycuda.autoinit
import pycuda.driver as drv
import pycuda.gpuarray as gpuarray
import skcuda.linalg as linalg
import skcuda.misc as misc
from pycuda.elementwise import ElementwiseKernel
import pycuda.cumath as cumath
import sys, getopt
import time

# El step_1 realiza la multiplicaci�n elemento a elemento de una banda con la pancrom�tica
def step_1(color_matrix, image_matrix):
    #La funciÃ³n linalg.mulitply realiza la multiplicaciÃ³n elemento a elemento entre dos matrices
    matrix_sal = linalg.multiply(color_matrix, image_matrix)
    return matrix_sal

# El step_2 determina el valor maximo y minimo de la banda resultante de la transformada de brovey
def step_2(matrix_1):
    mat_max = np.amax(matrix_1)
    mat_min = np.amin(matrix_1)
    return mat_max, mat_min


def step_3(matrix_1, matrix_color, mat_max, mat_min):
    #La funciÃ³n lin_comb invoca el kernel elementwise establecido para llevar a cabo el ajuste por rescale global min
    lin_comb(mat_min, matrix_1, mat_max, matrix_color)
    return matrix_color.get()


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
    # Convierte la pancromatica a float32
    panchromatic = panchromatic.astype(np.float32)
    # Suma las bandas de la multispectral
    msuma = r+g+b
    start=time.time()

    r_gpu = gpuarray.to_gpu(r)
    g_gpu = gpuarray.to_gpu(g)
    b_gpu = gpuarray.to_gpu(b)
    panchromatic_gpu = gpuarray.to_gpu(panchromatic)

    linalg.init()

    m33_gpu = step_1(r_gpu, panchromatic_gpu)
    m44_gpu = step_1(g_gpu, panchromatic_gpu)
    m55_gpu = step_1(b_gpu, panchromatic_gpu)

    Amax, Amin = step_2(m33_gpu.get())
    br_gpu = gpuarray.empty_like(r_gpu)
    br_host = step_3(m33_gpu, br_gpu, Amax, Amin)

    Amax, Amin = step_2(m44_gpu.get())
    bg_gpu = gpuarray.empty_like(g_gpu)
    bg_host = step_3(m44_gpu, bg_gpu, Amax, Amin)

    Amax, Amin = step_2(m55_gpu.get())
    bb_gpu = gpuarray.empty_like(b_gpu)
    bb_host = step_3(m55_gpu, bb_gpu, Amax, Amin)

    end = time.time()

    brr = br_host.astype(np.uint8)
    bgg = bg_host.astype(np.uint8)
    bbb = bb_host.astype(np.uint8)

    fusioned_image = np.stack((brr, bgg, bbb),axis=2)

    if(save_image):
        # Guarda la imagen resultando de acuerdo al tercer parametro establecido en la linea de ejecución del script
        if(savepath != None):
            t = skimage.io.imsave(savepath+'/multiplicativegpu_image.tif',fusioned_image, plugin='tifffile')
        else:
            t = skimage.io.imsave('multiplicativegpu_image.tif',fusioned_image, plugin='tifffile')
    #time_calculated de ejecución para la transformada de Brovey en GPU
    time_calculated = (end-start)
    if(timeCondition):
        return {"image": fusioned_image, "time" :  time_calculated}
    else:
        return fusioned_image
