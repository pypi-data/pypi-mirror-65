# main imports
import os
import numpy as np

# image imports
from PIL import Image


def rawls_to_pil(rawls_img):
    """Read and convert rawls image file into PIL image
    
    Arguments:
        rawls_img: {Rawls} .rawls image file loaded
    Returns:
        PIL RGB image

    Example:

    >>> import numpy as np
    >>> from rawls.converter import rawls_to_pil
    >>> from rawls.classes.rawls import Rawls
    >>> path = 'images/example.rawls'
    >>> rawls_img = Rawls.load(path)
    >>> rawls_pil_img = rawls_to_pil(rawls_img)
    >>> np.array(rawls_pil_img).shape
    (100, 100, 3)
    """
    rawls_img.gammaConvert()  # convert image to gamma if necessary

    return Image.fromarray(np.array(rawls_img.data, 'uint8'))


def rawls_to_png(rawls_img, outfile):
    """Convert rawls image into PNG image
    
    Arguments:
        rawls_img: {Rawls} rawls image object
        outfile: {str} output path of the .png image to save
    """

    if '/' in outfile:
        folders = outfile.split('/')
        del folders[-1]

        output_path = ''
        for folder in folders:
            output_path = os.path.join(output_path, folder)

        if not os.path.exists(output_path):
            os.makedirs(output_path)

    if '.png' not in outfile:
        raise Exception('output filename is not `.png` format')

    rawls_to_pil(rawls_img).save(outfile)
