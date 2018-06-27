import numpy as np
import utils.phased_array as pa


class TimeDelayBeamformer:

    attributes = ["wideband", "conventional"]

    def __init__(self, phased_array, steering_angle, c, fs):
        if not isinstance(phased_array, pa.PhasedArray):
            raise TypeError("Array must be a PhasedArray")
        self.array = phased_array
        self.fs = fs
        self.steeringAngle = steering_angle
        self.delay = np.zeros((self.array.sizeX, self.array.sizeY), float)
        self.weight = np.ones((self.array.sizeX, self.array.sizeY), float)
        self.c = c

    def compute_delays(self):
        """Compute the delays (in seconds) required on each mic unit to steer
        the beam in the desired angle."""
        #self.steeringAngle = steering_angle
        for x in range(0, self.array.sizeX):
            for y in range(0, self.array.sizeY):
                self.delay[x, y] = (1/self.c *
                                    np.sin(np.pi / 180. * self.steeringAngle[0]) *
                                    (np.cos(np.pi / 180. * self.steeringAngle[1]) * self.array.coordinatesY[y, x] +
                                     np.sin(np.pi / 180. * self.steeringAngle[1]) * self.array.coordinatesX[y, x]))

    def compute_weights(self, method='reset', argument=None):
        """Compute the tapering weights with a selected method."""
        # TODO : parse method ("reset", "Cheb", "Hamming", "Taylor", "Hann", "Kaiser", "custom"

        for x in range(0, self.array.sizeX):
            for y in range(0, self.array.sizeY):
                self.weight = 1.0

    @staticmethod
    def window_func(x, length):
        return 0.54 - 0.46 * np.cos(2.0 * np.pi * (x + 0.5) / length)

    def frac_delay(self, signal, delay, filter_length):
        tap_weight = np.zeros(filter_length, float)
        for t in range(0, filter_length):
            x = t - delay
            sinc = np.sinc(x - filter_length/2)
            tap_weight[t] = sinc * self.window_func(x, filter_length)
        return np.convolve(signal, tap_weight, 'same')

    def sec2spl(self, t):
        return self.fs * t

    def spl2sec(self, spl):
        return spl/self.fs

    def step(self, signal):
        self.compute_weights('reset', None)
        self.compute_delays()
        delayed_signal = self.frac_delay(signal, self.delay, 24)
        return delayed_signal.sum(axis=1)


class GSCBeamformer:

    attributes = ["wideband", "adaptive"]

    def __init__(self, phased_array, steering_angle, c, fs):
        if not isinstance(phased_array, pa.PhasedArray):
            raise TypeError("Array must be a PhasedArray")
        self.array = phased_array
        self.fs = fs
        self.steeringAngle = steering_angle
        self.delay = np.zeros((self.array.sizeX, self.array.sizeY), float)
        self.weight = np.ones((self.array.sizeX, self.array.sizeY), float)
        self.c = c
        self.blockingMatrix = np.zeros((self.array.size - 1, self.array.size))
        np.fill_diagonal(self.blockingMatrix, 1)
        np.fill_diagonal(np.rot90(np.rot90(self.blockingMatrix)), -1)

    def compute_delays(self):
        """Compute the delays (in seconds) required on each mic unit to steer
        the beam in the desired angle."""
        for x in range(0, self.array.sizeX):
            for y in range(0, self.array.sizeY):
                self.delay[y, x] = (1/self.c *
                                    np.sin(np.pi / 180. * self.steeringAngle[0]) *
                                    (np.cos(np.pi / 180. * self.steeringAngle[1]) * self.array.coordinatesX[y, x] +
                                     np.sin(np.pi / 180. * self.steeringAngle[1]) * self.array.coordinatesY[y, x]))

    def sec2spl(self, t):
        return self.fs * t

    def spl2sec(self, spl):
        return spl/self.fs

    def step(self, signal):
        """
        FBF | In Parallel?
        BM  |
           /
         /
        |
        MC
        """
        pass