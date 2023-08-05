"""Prediction Objects
Returned by models

JCA
Vaico
"""

class Object():
    __slots__ = ('geometry', 'label', 'score', 'subobject')

    def __init__(self,geometry=None, label=None, score=None, subobject=None ):
        self.geometry = geometry
        self.label = label
        self.score = score
        self.subobject = subobject

    def values(self):
        """Return tuple of object values"""
        return (self.geometry,self.label,self.score, self.subobject)

    def __eq__(self, other):
        return other.values() == self.values()

    def __repr__(self):
        class_name = type(self).__name__
        args_rep = str({i: getattr(self,i) for i in self.__slots__ })[1:-1]
        rep = '{}({})'.format(class_name, args_rep)
        return rep
