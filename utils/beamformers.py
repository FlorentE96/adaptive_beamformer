import numpy as np
import utils.phased_array as pa


class TimeDelayBeamformer:

    attributes = ["wideband", "conventional"]

    def __init__(self, phased_array, steering_angle, c):
        if not isinstance(phased_array, pa.PhasedArray):
            raise TypeError("Array must be a PhasedArray")
        self.array = phased_array
        self.steeringAngle = steering_angle
        self.delay = np.zeros((self.array.sizeX, self.array.sizeY), float)
        self.weight = np.ones((self.array.sizeX, self.array.sizeY), float)
        self.c = c

    def compute_delays(self):
        """Compute the delays (in seconds) required on each mic unit to steer the beam in the desired angle."""
        for x in range(0, self.array.sizeX):
            for y in range(0, self.array.sizeY):
                self.delay[x, y] = (1/self.c *
                                    np.sin(np.pi / 180. * self.steeringAngle[0]) *
                                    (np.cos(np.pi / 180. * self.steeringAngle[1]) * self.array.coordinatesX[x, y] +
                                     np.sin(np.pi / 180. * self.steeringAngle[1]) * self.array.coordinatesY[x, y]))

    def step(self):
        pass
