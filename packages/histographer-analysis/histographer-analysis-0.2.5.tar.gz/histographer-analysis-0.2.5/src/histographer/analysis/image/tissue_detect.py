from pathlib import Path
from histographer.analysis.image.color import rgb_to_normalized_hed
from histographer.analysis.image.segment import segment_rgb

import numpy as np
import cv2


def create_detector(image: np.ndarray):
    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()

    # Color to use (255 for detecting bright spots, 0 for detecting dark spots)
    params.blobColor = 255

    # Change thresholds
    params.minThreshold = 0
    params.maxThreshold = 255
    # params.maxThreshold = 200

    # Filter by Area.
    params.filterByArea = True
    params.minArea = 500
    params.maxArea = 9999999999999

    # Filter by Circularity
    params.filterByCircularity = False
    # params.minCircularity = 0.1

    # Filter by Convexity
    params.filterByConvexity = False
    # params.minConvexity = 0.87

    # Filter by Inertia
    params.filterByInertia = False
    # params.minInertiaRatio = 0.01

    # Create a detector with the parameters
    detector = cv2.SimpleBlobDetector_create(params)
    return detector


def tissue_detect(image: np.ndarray):
    """Use blob detection to find tissue"""
    detector: cv2.SimpleBlobDetector = create_detector(image)
    features = detector.detect(image)
    return features


if __name__ == '__main__':
    data_dir = Path(__file__).parents[4] / 'data' / 'alignment'
    print(data_dir.resolve())
    image = cv2.imread(str(data_dir / '1.png'))
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    print(image.dtype)
    image_hed = rgb_to_normalized_hed(image_rgb)
    print(image_hed.dtype)

    cv2.imshow('Window', image)
    cv2.waitKey(0)
    features = tissue_detect(image_hed[..., 1])
    im_with_keypoints = cv2.drawKeypoints(image, features, None, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imshow('Window', im_with_keypoints)
    cv2.imshow('E', image_hed[..., 1])
    cv2.waitKey(0)

