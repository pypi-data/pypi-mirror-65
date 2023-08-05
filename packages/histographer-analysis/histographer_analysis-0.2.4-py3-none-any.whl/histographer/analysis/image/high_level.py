"""High level functions for analyses"""

import numpy as np
import cv2

from typing import List, Dict

from histographer.analysis.image.color import rgb2hed, normalize_channels, channel_metrics
from histographer.analysis.image.segment import segment_sample
from histographer.analysis.image.fetch import get_images_with_annotations, ImageData
import histographer.analysis.image.analysis as analysis_module


def coloring_stats(rgb_images: List[np.ndarray]) -> List[Dict]:
    """Perform image segmentation and get coloring information for segmented areas.
    :param rgb_images: List of numpy arrays containing RGB images
    :return: List of dictionaries with results
    """
    results = []
    for image in rgb_images:
        image_results = {}

        # Convert RGB image to HED and normalize channels
        hed = rgb2hed(image)
        hed_n = normalize_channels(image)

        # Segment image into (nuclei, tissue, no_class)
        segments = segment_sample(hed_n)

        for name, seg in zip(('Nuclei H', 'Tissue E'), segments):
            metrics = channel_metrics(hed[seg])
            image_results[name] = metrics

        results.append(image_results)

    return results


def image_analysis(host_info: dict, annotation_ids: List[int], analyses: List[str]):
    """

    :param analyses:
    :param host_info: Dictionary with hosting information from secrets
    :param annotation_ids: List of annotation IDs to request from server
    :param analyses: List of analysis names
    :return:

    :raises ConnectionError: When images fail to fetch from server
    :raises ValueError: When analysis is unimplemented
    :raises RuntimeError: When images fail analysis
    """

    assert all(hasattr(analysis_module, an) for an in analyses)

    annotation_analyses = []
    for annotation_id in annotation_ids:
        cytomine_image = list(get_images_with_annotations(**host_info,
                                                          download=True,
                                                          annotation_ids=[annotation_id]).values())[0][0]
        image_data = ImageData(cytomine_image)
        d = {'annotationId': annotation_id, 'results': {
            an: getattr(analysis_module, an)(image_data)
            for an in analyses
        }}

        annotation_analyses.append(d)

    return annotation_analyses


if __name__ == '__main__':
    # image = cv2.imread('../data/muscular_tissue.png')
    # rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # print(coloring_stats([rgb_image]))

    from yaml import safe_load
    from pathlib import Path
    with open(Path(__file__).parents[4] / 'secrets.yml', 'r') as f:
        host_info = safe_load(f)['host']

    annotation_id = 1032341
    print(image_analysis(host_info, [annotation_id], ['he', 'hsv']))

