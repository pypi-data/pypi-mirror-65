from typing import Tuple
from collections import defaultdict as dd
from pathlib import Path

from skimage.color import rgb2hed
from cv2 import imshow, waitKey
from skimage.io import imread
import numpy as np

from cytomine import Cytomine
from cytomine.models.annotation import AnnotationCollection, Annotation

from histographer.analysis.image.color import normalize_channels
from histographer.analysis.image.segment import segment_sample


def get_images_with_annotations(host, public_key, private_key, project_id=None, download=True, annotation_ids=None):
    """
    Find and download (if not present) annotation information and images
    :param annotation_ids: List of annotations to fetch
    :param download: Whether or not to download missing files. Otherwise just fetches information.
    :param private_key: Private key as string
    :param public_key: Public key as string
    :param host: Hostname
    :param project_id: Restrict
    :return: List of dictionaries with 'image' and 'annotations'
    """
    output = []
    with Cytomine(host=host, public_key=public_key, private_key=private_key) as cytomine:
        annotations = AnnotationCollection()
        if project_id is not None:
            annotations.project = project_id

        annotations.fetch()
        print(f'{annotations}')

        image_regions = dd(list)

        for annotation in annotations:
            print(annotation)
            if annotation_ids is not None and annotation.id not in annotation_ids:
                continue
            print(f'Found annotation {annotation.id}')
            annotation: Annotation
            path = Path('/tmp') / 'cytomine' / 'p{project}' / 'i{image}' / 'masked{id}.png'
            formatted = str(path).format(id=annotation.id, image=annotation.image, project=annotation.project)
            print(f'Checking whether or not to download to {formatted}')
            if download and not Path(formatted).is_file():
                print(f'Dumping annotation to {formatted}')
                annotation.dump(str(path), override=True, mask=True, alpha=True)
                assert Path(formatted).is_file(), "Annotation image not found after download!"
            image_regions[annotation.image]\
                .append(formatted)

        print(image_regions)

        return image_regions


class ImageData:
    def __init__(self, local_path):
        self.local_path = local_path
        self._rgba = None
        self._rgb = None
        self._hed = None
        self._hed_norm = None
        self._segmentation = None
        self._mask = None

    @property
    def rgba(self):
        if self._rgba is None:
            self._rgba = imread(self.local_path)
            assert self._rgba.shape[-1] == 4, f'Transparency channel not read from {self.local_path}'

        return self._rgba

    @property
    def rgb(self) -> np.ndarray:
        if self._rgb is None:
            self._rgb = self.rgba[..., :3]

        return self._rgb

    @property
    def hed(self) -> np.ndarray:
        if self._hed is None:
            self._hed = rgb2hed(self.rgb)

        return self._hed

    @property
    def hed_norm(self):
        if self._hed_norm is None:
            self._hed_norm = normalize_channels(self.hed)

        return self._hed_norm

    @property
    def segmentation(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        if self._segmentation is None:
            self._segmentation = segment_sample(self.hed_norm)

        return self._segmentation

    @property
    def mask(self) -> np.ndarray:
        if self._mask is None:
            self._mask = self.rgba[..., 3].astype(bool)

        return self._mask


if __name__ == '__main__':
    from yaml import safe_load
    from pathlib import Path
    from skimage.color import rgb2hed
    from skimage.io import imread
    import numpy.ma as ma
    from histographer.analysis.image.segment import segment_plot_rgb
    from histographer.analysis.image.color import channel_metrics
    import numpy as np

    host = safe_load(open(Path(__file__).parents[4] / 'secrets.yml', 'r'))['host']
    image_regions = get_images_with_annotations(**host, download=True, annotation_ids=[1064743, 1064530])
    print(len(image_regions))
    print(image_regions)
    rgbas = [imread(im_url) for im_url in image_regions[next(iter(image_regions.keys()))]]
    #print(rgbas)
    imdat = ImageData(image_regions[385963][0])
    print(imdat.rgb)
    print(imdat.mask, imdat.hed)
    exit()

    i = 0
    im = rgbas[i]
    mask = im[..., 3]

    print('before mask')
    im[mask, :] = 0
    print('before segment')
    tissue, nuclei, no_class = segment_plot_rgb(im[..., :3])
    print('after segment')

    hed = rgb2hed(im[..., :3])

    print({
        'H': channel_metrics(ma.array(hed[..., 0], mask=(tissue & mask))),
        'E': channel_metrics(ma.array(hed[..., 1], mask=(nuclei & mask)))
    })

