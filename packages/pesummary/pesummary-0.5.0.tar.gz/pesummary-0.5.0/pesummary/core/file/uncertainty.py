
import numpy as np


class Uncertainty(object):
    def __init__(self, data, uncertainty):
        self.data = np.asarray(data)
        self.uncertainty = np.asarray(uncertainty)
        if len(self.data) != len(self.uncertainty):
            raise ValueError(
                "Please provide an uncertainty for each measurement"
            )
        if self.uncertainty.shape[1] != 2:
            raise ValueError(
                "Please provide an upper and lower bound for your measurement"
            )

    def __getitem__(self, num):
        return self.data[num]

    def __repr__(self):
        print("__repr__")
        return "no"

    def __str__(self):
        return "no"
