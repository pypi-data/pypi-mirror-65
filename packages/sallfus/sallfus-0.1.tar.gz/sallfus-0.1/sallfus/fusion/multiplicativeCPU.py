# -*- coding: utf-8 -*-
import skimage.io
import numpy as np
import cv2
import time
import sys, getopt

# El step_1 realiza la multiplicaciÃ³n elemento a elemento de una banda con la pancromÃ¡tica
def step_1(color_matrix, image_matrix):
    input_matrix = np.multiply(color_matrix,image_matrix)
    return input_matrix


# El step_2 determina el valor maximo y minimo de la banda resultante de la transformada de brovey
def step_2(matrix_1):
    mat_max = np.amax(matrix_1)
    mat_min = np.amin(matrix_1)
    return mat_max, mat_min


def step_3(matrix_1, mat_max, mat_min):
    matrix_color = np.empty_like(matrix_1)
    for m in range(matrix_1.shape[0]):
        for n in range(matrix_1.shape[0]):
            matrix_color[m,n] = (((matrix_1[m,n]-mat_min)*255)/(mat_max-mat_min))
    return matrix_color

end = 0
start = 0

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

    # Convierte a float32 y separa las bandas RGB de la multispectral
    multispectral = multispectral.astype(np.float32)
    r = multispectral[:,:,0].astype(np.float32)
    g = multispectral[:,:,1].astype(np.float32)
    b = multispectral[:,:,2].astype(np.float32)
    # Convierte la pancromatica a float32
    panchromatic = panchromatic.astype(np.float32)

    start = time.time()

    m33 = step_1(r, panchromatic)
    m44 = step_1(g, panchromatic)
    m55 = step_1(b, panchromatic)

    Amax, Amin = step_2(m33)
    br = step_3(m33, Amax, Amin)

    Amax, Amin = step_2(m44)
    bg = step_3(m44, Amax, Amin)

    Amax, Amin = step_2(m55)
    bb = step_3(m55, Amax, Amin)

    end = time.time()

    brr = br.astype(np.uint8)
    bgg = bg.astype(np.uint8)
    bbb = bb.astype(np.uint8)

    fusioned_image = np.stack((brr, bgg, bbb),axis=2)
    if(save_image):
        # Guarda la imagen resultando de acuerdo al tercer parametro establecido en la linea de ejecución del script
        if(savepath != None):
            t = skimage.io.imsave(savepath+'/multiplicativecpu_image.tif',fusioned_image, plugin='tifffile')
        else:
            t = skimage.io.imsave('multiplicativecpu_image.tif',fusioned_image, plugin='tifffile')
    #time_calculated de ejecución para la transformada de Brovey en GPU
    time_calculated = (end-start)
    if(timeCondition):
        return {"image": fusioned_image, "time" :  time_calculated}
    else:
        return fusioned_image
