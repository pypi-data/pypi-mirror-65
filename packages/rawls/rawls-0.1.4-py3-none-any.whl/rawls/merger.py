# main imports
import os
import numpy as np

# image imports
from PIL import Image

# stats import
from scipy.stats import skew, kurtosis

# class import
from .classes.rawls import Rawls
from .converter import rawls_to_png, rawls_to_pil


def _check_file_paths(filepaths):
    """check filepaths input extension
    
    Arguments:
        filepaths: {[str]} -- image filepaths list
    
    Raises:
        Exception: Need at least two .rawls image filepaths
        Exception: Invalid input filepaths extension
    """

    if len(filepaths) < 2:
        raise Exception('Need at least two rawls image filepaths as input')

    if not all(['.rawls' in p for p in filepaths]):
        raise Exception('Unvalid input filepath images, need .rawls image')


def merge_mean_rawls(filepaths):
    """Merge mean `.rawls` samples images from list of files
    
    Arguments:
        filepaths: {[str]} -- image filepaths list
    
    Returns:
        {Rawls} -- new rawls object with mean data of rawls files
    """

    # read rawls
    rawls_images = []

    for filepath in filepaths:
        rawls_images.append(Rawls.load(filepath))

    # getting and check shapes of images
    shapes = []

    _check_file_paths(filepaths)

    for img in rawls_images:
        shapes.append(img.shape)

    if not shapes[1:] == shapes[:-1]:
        raise Exception('Input rawls images do not have same shapes')

    # compute merge mean values
    merged_values = np.array([img.data for img in rawls_images])
    merged_values_mean = np.mean(merged_values, axis=0)

    # construct output data
    return Rawls(merged_values_mean.shape, merged_values_mean,
                 rawls_images[0].details)


def merge_mean_rawls_to_pil(filepaths):
    """Return mean merged image into RGB PIL
    
    Arguments:
        filepaths: {[str]} -- image filepaths list
    
    Returns:
        {PIL} -- RGB PIL mean merged image
    """
    merged_image = merge_mean_rawls(filepaths)
    return rawls_to_pil(merged_image)


def merge_mean_rawls_to_png(filepaths, outfile):
    """Save mean merged image into PNG
    
    Arguments:
        filepaths: {[str]} -- image filepaths list
        outfile: {str} -- output path of the .png image to save
    """
    merged_image = merge_mean_rawls(filepaths)
    rawls_to_png(merged_image, outfile)


def merge_var_rawls(filepaths):
    """Merge variance `.rawls` samples images from list of files
    
    Arguments:
        filepaths: {[str]} -- image filepaths list
    
    Returns:
        {Rawls} -- new rawls object with variance data of rawls files
    """

    # read rawls
    rawls_images = []

    _check_file_paths(filepaths)

    for filepath in filepaths:
        rawls_images.append(Rawls.load(filepath))

    # getting and check shapes of images
    shapes = []

    for img in rawls_images:
        shapes.append(img.shape)

    if not shapes[1:] == shapes[:-1]:
        raise Exception('Input rawls images do not have same shapes')

    # compute merge var values
    merged_values = np.array([img.data for img in rawls_images])
    merged_values_var = np.var(merged_values, axis=0)

    # construct output data
    return Rawls(merged_values_var.shape, merged_values_var,
                 rawls_images[0].details)


def merge_var_rawls_to_pil(filepaths):
    """Return var merged image into RGB PIL
    
    Arguments:
        filepaths: {[str]} -- image filepaths list
    
    Returns:
        {PIL} -- RGB PIL var merged image
    """
    merged_image = merge_var_rawls(filepaths)
    return rawls_to_pil(merged_image)


def merge_var_rawls_to_png(filepaths, outfile):
    """Save variance merged image into PNG
    
    Arguments:
        filepaths: {[str]} -- image filepaths list
        outfile: {str} -- output path of the .png image to save
    """
    merged_image = merge_var_rawls(filepaths)
    return rawls_to_png(merged_image, outfile)


def merge_std_rawls(filepaths):
    """Merge std `.rawls` samples images from list of files
    
    Arguments:
        filepaths: {[str]} -- image filepaths list
    
    Returns:
        {Rawls} -- new rawls object with std data of rawls files
    """

    # read rawls
    rawls_images = []

    _check_file_paths(filepaths)

    for filepath in filepaths:
        rawls_images.append(Rawls.load(filepath))

    # getting and check shapes of images
    shapes = []

    for img in rawls_images:
        shapes.append(img.shape)

    if not shapes[1:] == shapes[:-1]:
        raise Exception('Input rawls images do not have same shapes')

    # compute merge std values
    merged_values = np.array([img.data for img in rawls_images])
    merged_values_var = np.std(merged_values, axis=0)

    # construct output data
    return Rawls(merged_values_var.shape, merged_values_var,
                 rawls_images[0].details)


def merge_std_rawls_to_pil(filepaths):
    """Return std merged image into RGB PIL
    
    Arguments:
        filepaths: {[str]} -- image filepaths list
    
    Returns:
        {PIL} -- RGB PIL std merged image
    """
    merged_image = merge_std_rawls(filepaths)
    return rawls_to_pil(merged_image)


def merge_std_rawls_to_png(filepaths, outfile):
    """Save std merged image into PNG
    
    Arguments:
        filepaths: {[str]} -- image filepaths list
        outfile: {str} -- output path of the .png image to save
    """
    merged_image = merge_std_rawls(filepaths)
    return rawls_to_png(merged_image, outfile)


def merge_skew_rawls(filepaths):
    """Merge skew `.rawls` samples images from list of files
    
    Arguments:
        filepaths: {[str]} -- image filepaths list
    
    Returns:
        {Rawls} -- new rawls object with skew data of rawls files
    """

    # read rawls
    rawls_images = []

    _check_file_paths(filepaths)

    for filepath in filepaths:
        rawls_images.append(Rawls.load(filepath))

    # getting and check shapes of images
    shapes = []

    for img in rawls_images:
        shapes.append(img.shape)

    if not shapes[1:] == shapes[:-1]:
        raise Exception('Input rawls images do not have same shapes')

    # compute merge var values
    merged_values = np.array([img.data for img in rawls_images])
    merged_values_skew = skew(merged_values, axis=0, nan_policy='raise')

    # construct output data
    return Rawls(merged_values_skew.shape, merged_values_skew,
                 rawls_images[0].details)


def merge_kurtosis_rawls(filepaths):
    """Merge kurtosis `.rawls` samples images from list of files
    
    Arguments:
        filepaths: {[str]} -- image filepaths list
    
    Returns:
        {Rawls} -- new rawls object with kurtosis data of rawls files
    """

    # read rawls
    rawls_images = []

    _check_file_paths(filepaths)

    for filepath in filepaths:
        rawls_images.append(Rawls.load(filepath))

    # getting and check shapes of images
    shapes = []

    for img in rawls_images:
        shapes.append(img.shape)

    if not shapes[1:] == shapes[:-1]:
        raise Exception('Input rawls images do not have same shapes')

    # compute merge var values
    merged_values = np.array([img.data for img in rawls_images])
    merged_values_kurtosis = kurtosis(
        merged_values, axis=0, nan_policy='raise')

    # construct output data
    return Rawls(merged_values_kurtosis.shape, merged_values_kurtosis,
                 rawls_images[0].details)


def merge_skew_norm_rawls(filepaths):
    """Compute skewness from .rawls files and normalize data
    
    Arguments:
        filepaths: {[str]} image filepaths list
    
    Returns:
        {Rawls} -- new rawls object with skewness normalized data of rawls files
    """

    merged_rawls = merge_skew_rawls(filepaths)
    img_skew_0 = merged_rawls.data + abs(np.min(merged_rawls.data))
    img_skew_norm = img_skew_0 / np.max(img_skew_0)

    merged_rawls.data = img_skew_norm

    return merged_rawls


def merge_kurtosis_norm_rawls(filepaths):
    """Compute kurtosis from .rawls files and normalize data
    
    Arguments:
        filepaths: {[str]} image filepaths list
    
    Returns:
        {Rawls} -- new rawls object with kurtosis normalized data of rawls files
    """

    merged_rawls = merge_kurtosis_rawls(filepaths)
    img_skew_0 = merged_rawls.data + abs(np.min(merged_rawls.data))
    img_skew_norm = img_skew_0 / np.max(img_skew_0)

    merged_rawls.data = img_skew_norm

    return merged_rawls
