from MLgeometry.geometries.Geometry import Geometry

class BoundBox(Geometry):

    __slots__ = ('xmin', 'ymin', 'xmax', 'ymax')

    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

    def centroid(self):
        return (self.xmin + (self.xmax - self.xmin)/2,
                self.ymin + (self.ymax - self.ymin)/2)

    def _asdict(self):
        return {
            'xmin' : self.xmin,
            'xmax' : self.xmax,
            'ymin' : self.ymin,
            'ymax' : self.ymax,
        }

    @classmethod
    def _fromdict(cls, info_dict):
        return cls(
            float(info_dict['xmin']),
            float(info_dict['ymin']),
            float(info_dict['xmax']),
            float(info_dict['ymax']),
        )

    def __iter__(self):
        return (i for i in (self.xmin,self.ymin,self.xmax,self.ymax))


if __name__ == '__main__':
    a = BoundBox(1,2,3,4)
    print(a.xmin)
