# -*- coding: utf-8 -*-
from sallfus.fusion import broveyCPU
from sallfus.fusion import broveyGPU
from sallfus.fusion import multiplicativeCPU
from sallfus.fusion import multiplicativeGPU
from sallfus.fusion import atrousCPU
from sallfus.fusion import atrousGPU
from sallfus.fusion import pcaCPU
from sallfus.fusion import pcaGPU
from sallfus.measures import mse, rmse, correlation_coeff, bias
import sys

def generated_method(method):
    if(method == 'brovey'):
        array_method = [broveyCPU, broveyGPU]
    elif(method == 'multiplicative'):
        array_method = [multiplicativeCPU, multiplicativeGPU]
    elif(method == 'pca'):
        array_method = [pcaCPU, pcaGPU]
    elif(method == 'atrous'):
        array_method = [atrousCPU, atrousGPU]
    else:
         sys.exit('The method is invalid')
    return array_method


def time_comparison(multispectral, panchromatic, method):
    results = dict()
    array_types = ['cpu','gpu']
    if(type(method) != str):
        sys.exit('Methods must be a string')
    method_array = generated_method(method)
    for i in range(len(method_array)):
        result_temp = method_array[i].fusion_images(multispectral, panchromatic)
        results.update({method+'_'+array_types[i] : result_temp['time']})
    return results


def generated_measures(measures):
    array_measures = []
    for i in range(len(measures)):
        if(measures[i] == 'mse'):
            array_measures.append(mse)
        elif(measures[i] == 'rmse'):
            array_measures.append(rmse)
        elif(measures[i] == 'cc'):
            array_measures.append(correlation_coeff)
        elif(measures[i] == 'bias'):
            array_measures.append(bias)
        else:
             sys.exit('The measure is invalid')
    return array_measures

def measures_comparison(fusioned, original, measures):
    results = dict()
    results_temp_dict = dict()
    real_measures = generated_measures(measures)
    for i in range(len(real_measures)):
        result_temp = real_measures[i](fusioned, original)
        results_temp_dict.update({'R':result_temp[0], 'G':result_temp[1], 'B':result_temp[2]})
        results.update({measures[i] : results_temp_dict})
        results_temp_dict = dict() 
    return results

def generated_methods(methods):
    array_methods = []
    array_names = []
    for i in range(len(methods)):
        if(methods[i] == 'brovey'):
            array_methods.append(broveyCPU)
            array_methods.append(broveyGPU)
            array_names.append('broveyCPU')
            array_names.append('broveyGPU')
        elif(methods[i] == 'multiplicative'):
            array_methods.append(multiplicativeCPU)
            array_methods.append(multiplicativeGPU)
            array_names.append('multiplicativeCPU')
            array_names.append('multiplicativeGPU')
        elif(methods[i] == 'pca'):
            array_methods.append(pcaCPU)
            array_methods.append(pcaGPU)
            array_names.append('pcaCPU')
            array_names.append('pcaGPU')
        elif(methods[i] == 'atrous'):
            array_methods.append(atrousCPU)
            array_methods.append(atrousGPU)
            array_names.append('atrousCPU')
            array_names.append('atrousGPU')
        else:
             sys.exit('The methods are invalid')
    return array_methods, array_names

def time_comparison_multiple(multispectral, panchromatic, methods):
    results = dict()
    array_types = ['cpu','gpu']
    methods_array, names_array = generated_methods(methods)
    for i in range(len(methods_array)):
        result_temp = methods_array[i].fusion_images(multispectral, panchromatic)
        results.update({names_array[i] : result_temp['time']})
    return results
