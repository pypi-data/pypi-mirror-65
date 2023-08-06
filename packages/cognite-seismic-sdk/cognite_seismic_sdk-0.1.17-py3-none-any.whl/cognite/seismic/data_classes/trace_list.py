# Copyright 2019 Cognite AS

import itertools

import numpy as np

from cognite.seismic.data_classes.custom_list import CustomList


class Trace3DList(CustomList):
    def to_array(self):
        self.load()
        new_list = [list(g) for k, g in itertools.groupby(self, lambda x: x.iline.value)]
        result = []
        for inline_group in new_list:
            result.append(np.array([np.array(i.trace) for i in inline_group]))
        return np.array(result)


class Trace2DList(CustomList):
    def to_array(self):
        self.load()
        return np.array([np.array(t.trace) for t in self])
