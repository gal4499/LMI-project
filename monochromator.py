import numpy as np
from main import *
import matplotlib.pyplot as plt
from functions import *

lambda0 = 8.33e-4  # grating period
R = 400 # focal length of lenses
ψ = np.radians(-90)  # incident angle to grating surface

#frequency_spectrum = (10 ** 12) * np.linspace(400, 790, num=50)  # visible light spectrum
frequency_spectrum = (10 ** 12) * np.array([450, 550, 650])
angle_spectrum = np.linspace(-0.2, -0.15, num=5)
colors = plt.cm.gist_rainbow(np.linspace(0, 1, len(frequency_spectrum)+1))
#colors = plt.cm.gist_rainbow(np.linspace(0, 1, 8))

def one_pass_mask(vmin, vmax, frequency_spectrum):
    transfer_vector = np.zeros(len(frequency_spectrum))
    for i in range(len(frequency_spectrum)):
        v = frequency_spectrum[i]
        if vmin <= v <= vmax :
            transfer_vector[i] = 1
    return transfer_vector

for i in range(len(frequency_spectrum)):
#for i in range(1):
    v = frequency_spectrum[i]
    t = 0
    x = 0
    mirror_matrix = lens_matrix(R/2)
    grating_matrix = grating(ψ, lambda0, v)
    free_space_matrix1 = free_space(200, v)
    free_space_matrix2 = free_space(100, v)

    for j in range(len(angle_spectrum)):
    #for j in range(1):
        θ = angle_spectrum[j]
        #θ = -0.05

        initial_vector = np.transpose(np.array([x, θ, t, v]))
        before_mirror_vector = np.dot(free_space_matrix1, initial_vector)
        mirror_vector = np.dot(mirror_matrix, before_mirror_vector)
        before_grating_vector = np.dot(free_space_matrix2, mirror_vector)
        grating_vector = np.dot(grating_matrix, before_grating_vector)
        before_mirror_vector2 = np.dot(free_space_matrix2, grating_vector)
        mirror_vector2 = np.dot(mirror_matrix, before_mirror_vector2)
        after_mirror_vector = np.dot(free_space_matrix1, mirror_vector2)

        x_before_mirror = before_mirror_vector[0]
        x_before_grating = before_grating_vector[0]
        x_before_mirror2 = before_mirror_vector2[0]
        x_after_mirror = after_mirror_vector[0]

        plt.plot([0, 200, 100, 200, 0], [x, x_before_mirror, x_before_grating, x_before_mirror2, x_after_mirror] , color=colors[i])

plt.title("Czerny-Turner Monochromator")
plt.xlabel("z - optical axis [mm]")
plt.ylabel("x [mm]")
plt.grid()
plt.show()