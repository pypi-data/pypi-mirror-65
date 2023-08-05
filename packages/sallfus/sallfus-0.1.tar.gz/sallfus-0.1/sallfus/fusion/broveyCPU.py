# -*- coding: utf-8 -*-
import skimage.io
import numpy as np
import cv2
import sys, getopt
import time


# El step_1 realiza la la división de la banda entre la suma de las bandas
def step_1(matrix_1, matrix_color, msuma_matrix):
    for m in range(matrix_1.shape[0]):
        for n in range(matrix_1.shape[0]):
            if (msuma_matrix[m,n] != 0):
                matrix_1[m,n] = (3*matrix_color[m,n])/msuma_matrix[m,n]
            else:
                matrix_1[m,n] = msuma_matrix[m,n]
    return matrix_1

# El step_2 realiza la multiplicación posición a posición del step_1 por la pancromatica
def step_2(matrix_1, matrix_2, matrix_image_pan):
    for m in range(matrix_2.shape[0]):
        for n in range(matrix_2.shape[0]):
            matrix_2[m,n] = matrix_1[m,n]*matrix_image_pan[m,n]
    return matrix_2

# El step_3 determina el valor maximo y minimo de la banda resultante de la transformada de brovey
def step_3(matrix_1):
    mat_max = np.amax(matrix_1)
    mat_min = np.amin(matrix_1)
    return mat_max, mat_min

# El step_4 realiza un ajuste de riqueza espectral llamado rescale global min
def step_4(matrix_1, matrix_color, mat_max, mat_min):
    for m in range(matrix_color.shape[0]):
        for n in range(matrix_color.shape[0]):
            matrix_color[m,n] = (((matrix_1[m,n]-mat_min)*255)/(mat_max-mat_min))
    return matrix_color


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
    m1 = multispectral.astype(np.float32)
    r = multispectral[:,:,0]
    r1 = r.astype(np.float32)
    g = multispectral[:,:,1]
    g1 = g.astype(np.float32)
    b = multispectral[:,:,2]
    b1 = b.astype(np.float32)
    # Convierte la pancromatica a float32
    p1 = panchromatic.astype(np.float32)
    msuma = r1+g1+b1
    start=time.time()
    m11 = np.zeros_like(r1)
    m11 = step_1(m11, r1, msuma)
    m22 = np.zeros_like(g1)
    m22 = step_2(m11, m22, p1)
    m33 = np.zeros_like(b1)
    m33 = step_1(m33, b1, msuma)
    m44 = np.zeros_like(b1)
    m44 = step_2(m33, m44, p1)
    m55 = np.zeros_like(g1)
    m55 = step_1(m55, g1, msuma)
    m66 = np.zeros_like(g1)
    m66 = step_2(m55, m66, p1)
    Amax, Amin = step_3(m22)
    rr = np.zeros_like(r1)
    rr = step_4(m22, rr, Amax, Amin)
    Amax, Amin = step_3(m66)
    gg = np.zeros_like(g1)
    gg = step_4(m66, gg, Amax, Amin)
    Amax, Amin = step_3(m44)
    bb = np.zeros_like(b1)
    bb = step_4(m44, bb, Amax, Amin)
    end = time.time()
    rrr = rr.astype(np.uint8)
    ggg = gg.astype(np.uint8)
    bbb = bb.astype(np.uint8)
    # Combina las bandas resultantes
    fusioned_image = np.stack((rrr, ggg, bbb),axis=2)
    if(save_image):
        # Guarda la imagen resultando de acuerdo al tercer parametro establecido en la linea de ejecución del script
        if(savepath != None):
            t = skimage.io.imsave(savepath+'/broveycpu_image.tif',fusioned_image, plugin='tifffile')
        else:
            t = skimage.io.imsave('broveycpu_image.tif',fusioned_image, plugin='tifffile')
    #time_calculated de ejecución para la transformada de Brovey en GPU
    time_calculated = (end-start)
    if(timeCondition):
        return {"image": fusioned_image, "time" :  time_calculated}
    else:
        return fusioned_image
