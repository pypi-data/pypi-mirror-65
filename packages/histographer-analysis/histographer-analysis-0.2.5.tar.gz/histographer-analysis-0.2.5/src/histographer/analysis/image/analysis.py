from numpy import ma
from skimage.color import rgb2hsv

from histographer.analysis.image.color import channel_metrics
from histographer.analysis.image.fetch import ImageData

# All function names in this file can be used as analysis ids. Must take in ImageData and return nested dictionary of
# results


def he(im: ImageData):
    tissue, nuclei, no_class = im.segmentation
    mask, hed = im.mask, im.hed

    return {
        'H': channel_metrics(ma.array(hed[..., 0], mask=(tissue & mask))),
        'E': channel_metrics(ma.array(hed[..., 1], mask=(nuclei & mask)))
    }


def hsv(im: ImageData):
    hsv = rgb2hsv(im.rgb)
    mask = im.mask
    return {
        channel_name: channel_metrics(ma.array(hsv[..., i], mask=mask))
        for i, channel_name in enumerate('HSV')
    }
