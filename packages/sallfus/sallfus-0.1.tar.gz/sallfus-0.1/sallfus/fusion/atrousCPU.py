# -*- coding: utf-8 -*-
import skimage.io
from skimage.color import rgb2hsv, hsv2rgb
from scipy import ndimage
import numpy as np
import sys
import time

def adjust_values(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if(matrix[i][j] < 0):
                matrix[i][j] = 0
    return matrix

def hist_match(source, template):
    """
    Adjust the pixel values of a grayscale image such that its histogram
    matches that of a target image

    Arguments:
    -----------
        source: np.ndarray
            Image to transform; the histogram is computed over the flattened
            array
        template: np.ndarray
            Template image; can have different dimensions to source
    Returns:
    -----------
        matched: np.ndarray
            The transformed output image
    """

    oldshape = source.shape
    source = source.ravel()
    template = template.ravel()

    # get the set of unique pixel values and their corresponding indices and
    # counts
    s_values, bin_idx, s_counts = np.unique(source, return_inverse=True,
                                            return_counts=True)
    t_values, t_counts = np.unique(template, return_counts=True)

    # take the cumsum of the counts and normalize by the number of pixels to
    # get the empirical cumulative distribution functions for the source and
    # template images (maps pixel value --> quantile)
    s_quantiles = np.cumsum(s_counts).astype(np.float64)
    s_quantiles /= s_quantiles[-1]
    t_quantiles = np.cumsum(t_counts).astype(np.float64)
    t_quantiles /= t_quantiles[-1]

    # interpolate linearly to find the pixel values in the template image
    # that correspond most closely to the quantiles in the source image
    interp_t_values = np.interp(s_quantiles, t_quantiles, t_values)

    return interp_t_values[bin_idx].reshape(oldshape)



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


    start=time.time()
    hsv = rgb2hsv(multispectral)
    val = hsv[:,:,2]
    sat = hsv[:,:,1]
    mat = hsv[:,:,0]

    pani = hist_match(panchromatic,val)

    s = np.array([[1/256, 1/64, 3/128, 1/64, 1/256],[1/64, 1/16, 3/32, 1/16, 1/64],[3/128, 3/32, 9/64, 3/32, 3/128],
                    [1/64, 1/16, 3/32, 1/16, 1/64],[1/256, 1/64, 3/128, 1/64, 1/256]])
    I1 = ndimage.correlate(pani, s, mode='constant')

    s1 = np.array([[1/256, 0, 1/64, 0, 3/128, 0, 1/64, 0, 1/256],[0, 0, 0, 0, 0, 0, 0, 0, 0],[1/64, 0, 1/16, 0, 3/32, 0, 1/16, 0, 1/64],[0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [3/128, 0, 3/32, 0, 9/64, 0, 3/32, 0, 3/128],[0, 0, 0, 0, 0, 0, 0, 0, 0],[1/64, 0, 1/16, 0, 3/32, 0, 1/16, 0, 1/64], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [1/256, 0, 1/64, 0, 3/128, 0, 1/64, 0, 1/256]])
    I2 = ndimage.correlate(I1, s1, mode='constant')

    W1=(pani-I1)
    W1 = adjust_values(W1)
    W1 = W1.astype(np.uint8)

    W2=(I1-I2)
    W2 = adjust_values(W2)
    W2 = W2.astype(np.uint8)

    nint=(panchromatic+W1+W2).astype(np.uint8)

    end = time.time()

    n_hsv1 = np.stack((mat, sat, nint),axis=2)
    n_hsv = n_hsv1
    fusioned_image = hsv2rgb(n_hsv).astype(np.uint8)
    if(save_image):
        # Guarda la imagen resultando de acuerdo al tercer parametro establecido en la linea de ejecución del script
        if(savepath != None):
            t = skimage.io.imsave(savepath+'/atrouscpu_image.tif',fusioned_image, plugin='tifffile')
        else:
            t = skimage.io.imsave('atrouscpu_image.tif',fusioned_image, plugin='tifffile')
    #time_calculated de ejecución para la transformada de Brovey en GPU
    time_calculated = (end-start)
    if(timeCondition):
        return {"image": fusioned_image, "time" :  time_calculated}
    else:
        return fusioned_image
