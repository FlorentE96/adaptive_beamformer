import cv2 as cv
import numpy as np
import utils.phased_array as pa
import utils.beamformers as bf
import matplotlib.pyplot as plt
from scipy.io import wavfile

fs, data = wavfile.read('./media/simulated.wav')

ang_dft = np.array([-30, -20], float)

myArray = pa.URA(4, 4, 0.042, 0.042)
TDBeamformer = bf.TimeDelayBeamformer(myArray, ang_dft, 320.0)

myArray.plot_array()
TDBeamformer.compute_delays()

print(TDBeamformer.delay)
print(myArray.coordinatesX)
print(myArray.coordinatesY)

plt.show()