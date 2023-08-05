from typing import Tuple

from skimage.color import rgb2hed
from histographer.analysis.image.color import normalize_channels
import matplotlib.pyplot as plt
import cv2
import numpy as np

default_parameters = {'cutoff_nucleus': 160, 'cutoff_tissue': 140}


def segment_rgb(rgb: np.ndarray, parameters=None) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Returns (tissue, nucleus, no_class)
    :param rgb: RGB NumPy array
    :param parameters:
    :return: A tuple of NumPy arrays (Tissue, Nucleus, N_class)
    """
    return segment_sample(normalize_channels(rgb2hed(rgb)), parameters=parameters)


def segment_sample(normalized_hed: np.ndarray, parameters=None) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Returns (tissue, nucleus, no_class)
    :param normalized_hed: NumPy array with normalized HED channels
    :param parameters: Dictionary of parameters used in to segment images.
    :return: A tuple of NumPy arrays (Tissue, Nucleus, N_class)
    """
    hed = normalized_hed
    if parameters is None:
        parameters = default_parameters

    # Find tissue
    tissue: np.ndarray = hed[..., 1] > parameters['cutoff_tissue']
    nucleus: np.ndarray = hed[..., 0] > parameters['cutoff_nucleus']
    tissue[nucleus] = 0

    no_class: np.ndarray = ~(tissue | nucleus)

    return tissue, nucleus, no_class


def segment_plot_rgb(rgb: np.ndarray):
    plt.imshow(rgb)
    plt.show()
    rgb = rgb.copy()
    tissue, nuclei, no_class = segment_rgb(rgb)
    rgb[tissue, ...] = [255, 0, 0]
    rgb[nuclei, ...] = [0, 255, 0]
    rgb[no_class, ...] = [0, 0, 255]
    plt.imshow(rgb)
    plt.show()
    return tissue, nuclei, no_class


if __name__ == '__main__':
    def nothing(x):
        pass


    winname = 'Bayesian Classifier'

    # Create a black image, a window
    cv2.namedWindow(winname)

    # create trackbars for color change
    cv2.createTrackbar('Cutoff Nucleus', winname, 0, 255, nothing)
    cv2.createTrackbar('Cutoff Tissue', winname, 0, 255, nothing)

    tissue = cv2.imread('../../../../data/muscular_tissue.png')
    cv2.imshow('Tissue', tissue)
    hed = rgb2hed(cv2.cvtColor(tissue, cv2.COLOR_BGR2RGB))

    # Normalize channels
    hedn = normalize_channels(hed)

    img = tissue.copy()
    while True:
        cv2.imshow(winname, img)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

        # get current positions of four trackbars
        cn = cv2.getTrackbarPos('Cutoff Nucleus', winname)
        ct = cv2.getTrackbarPos('Cutoff Tissue', winname)
        print(cn, ct)

        img[:] = tissue.copy()
        img[hedn[..., 1] > ct, ...] = [0, 0, 255]
        img[hedn[..., 0] > cn, ...] = [0, 255, 0]

    cv2.destroyAllWindows()
