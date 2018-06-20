import numpy as np
import matplotlib.pyplot as plt


class PhasedArray:

    type = None

    def __init__(self):
        self.index = None
        self.sizeX, self.sizeY = None, None
        self.spaceX, self.spaceY = None, None
        self.indexX, self.indexY = None, None
        self.coordinatesX, self.coordinatesY = None, None

    def plot_array(self):
        pass


class URA(PhasedArray):

    type = "linear"

    def __init__(self, size_x, size_y, space_x, space_y):
        super(URA, self).__init__()
        self.sizeX, self.sizeY = size_x, size_y
        self.spaceX, self.spaceY = space_x, space_y
        self.indexX = np.arange(self.sizeX)*self.spaceX
        self.indexY = np.arange(self.sizeY)*self.spaceY
        self.coordinatesX, self.coordinatesY = np.meshgrid(self.indexX, self.indexY)
        self.coordinatesX -= (self.sizeX-1)/2 * self.spaceX
        self.coordinatesY -= (self.sizeY - 1) / 2 * self.spaceY

    def plot_array(self):
        plt.plot(self.coordinatesX, self.coordinatesY, marker='o', color='k', linestyle='none')
        plt.draw()
