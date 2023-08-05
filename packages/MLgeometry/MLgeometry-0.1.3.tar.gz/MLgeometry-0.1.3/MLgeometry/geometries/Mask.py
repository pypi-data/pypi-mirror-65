"""
Mask Geometry
**Mask is an image (Matrix) that defines which pixel belongs to a class

Parameters:
- mask (ndarray): The parameter mask is a boolean matrix of 2 dimensions
corresponding only to one class
- roi (tuple or list of tuples) boundbox of the region (y1, x1, y2, x2)

MaskRCNN Output:
rois: [N, (y1, x1, y2, x2)] detection bounding boxes
class_ids: [N] int class IDs
scores: [N] float probability scores for the class IDs
masks: [H, W, N] instance binary masks

JCA
Vaico
"""
import reprlib

import numpy as np
from _collections import namedtuple

from MLgeometry.geometries.Geometry import Geometry


class Mask(Geometry):
    __slots__ = ('idx', 'roi', 'shape')

    def __init__(self, mask, roi, idx=None, shape=None):
        """
        :mask: (ndarray): Boolean matrix of 2 dimensions
        :roi: (tuple or list of tuples) bound box coordinates (y1, x1, y2, x2)
        """
        if idx:
            # When is instantiated from a dict
            self.idx = idx
            self.shape = shape
        else:
            # Get only the index of flatten mask (converted into array)
            mask = mask.astype(bool)
            flat = mask.flatten()
            self.idx = np.where(flat == True)[0].tolist()
            self.shape = mask.shape

        if not isinstance(roi, list):
            self.roi = roi.tolist()
        else:
            self.roi = roi

    def __iter__(self):
        return iter(self.idx)

    def calc_c(self, coords):
        return ((coords[1] + (coords[3] - coords[1])/2,
                coords[0] + (coords[2] - coords[0])/2))

    def centroid(self):
        centers = []
        if isinstance(self.roi, list):
            for r in range(len(self.roi)):
                centers.append(self.calc_c(self.roi[r]))
        else:
            centers.append(self.calc_c(self.roi))
        return centers

    def _asdict(self):
        return {
            'idx': self.idx,
            'shape': self.shape,
            'roi': self.roi
        }

    def __len__(self):
        return len(self.idx)

    @classmethod
    def _fromdict(cls, info_dict):
        return cls(None,
                   info_dict['roi'],
                   idx=info_dict['idx'],
                   shape=info_dict['shape'])

    def __eq__(self, other):
        return self.idx == self.idx and self.shape == self.shape

    def __repr__(self):
        class_name = type(self).__name__
        args = {
            'idx': self.idx
        }
        return '{}({})'.format(class_name, reprlib.repr(args))
