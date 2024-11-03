import numpy as np
from main import *
import matplotlib.pyplot as plt
from functions import *
from math import ceil

lambda0 = 3e-3  # grating period
f = 300  # focal length of lenses
ψ = np.radians(30)  # incident angle to grating surface

frequency_spectrum = (10 ** 12) * np.linspace(400, 790, num=500)  # visible light spectrum
time_domain_pulse = (10 ** (-15)) * np.linspace(0, 10, num=500)  # rectangular time pulse
#space_domain_pulse = np.full(len(time_domain_pulse), 0)   # option A - all rays start from the same point in space
space_domain_pulse = (10 ** (-4)) * np.linspace(0, 8, num=500)  # option B - rectangular space pulse
colors = plt.cm.gist_rainbow(np.linspace(0, 1, len(frequency_spectrum)))

# define binary masks
def slit_mask(bit_num, frequency_spectrum, xmin, xmax, vectors_matrix):
    transfer_vector = np.zeros(len(frequency_spectrum))
    bit_vector = np.linspace(xmin, xmax, bit_num)
    for i in range(bit_num):
        if i % 2 == 0:
            for j in range(len(frequency_spectrum)):
                if bit_vector[i] <= vectors_matrix[0, j] < bit_vector[i+1]:
                    transfer_vector[j] = 1
    return transfer_vector

def one_pass_mask(vmin, vmax, frequency_spectrum):
    transfer_vector = np.zeros(len(frequency_spectrum))
    for i in range(len(frequency_spectrum)):
        v = frequency_spectrum[i]
        if vmin <= v <= vmax :
            transfer_vector[i] = 1
    return transfer_vector

def one_doesnt_pass_mask(vmin, vmax, frequency_spectrum):
    transfer_vector = np.full(len(frequency_spectrum), 1)
    for i in range(len(frequency_spectrum)):
        v = frequency_spectrum[i]
        if vmin <= v <= vmax :
            transfer_vector[i] = 0
    return transfer_vector

vectors_matrix = np.zeros((4, len(space_domain_pulse)))  # matrix to store all the vectors in the fourier plane later
for i in range(len(frequency_spectrum)):
    v = frequency_spectrum[i]
    grating_matrix = grating(ψ, lambda0, v)
    free_space_matrix = free_space(f, v)
    lens = lens_matrix(f)
    t = time_domain_pulse[i]
    x = space_domain_pulse[i]

    initial_vector = np.transpose(np.array([x, 0, t, v]))
    grating_vector = np.dot(grating_matrix, initial_vector)
    after_grating_vector = np.dot(free_space_matrix, grating_vector)
    lens_vector = np.dot(lens, after_grating_vector)
    fourier_plane_vector = np.dot(free_space_matrix, lens_vector)

    vectors_matrix[:, i] = fourier_plane_vector

    x_initial = space_domain_pulse[i]
    x_after_grating = after_grating_vector[0]
    x_fourier = fourier_plane_vector[0]

    plt.plot([0, f, 2 * f], [x_initial, x_after_grating, x_fourier], color=colors[i])

xmin = min(vectors_matrix[0, :])  #find limits for mask
xmax = max(vectors_matrix[0, :])
bit_num = 10  # number of bits, used for a binary amplitude mask
vmin = (10 ** 12) * 530  # angular frequency range for mask
vmax = (10 ** 12) * 600

# choose wanted mask, keep the others as comments:

#transfer_vector = slit_mask(bit_num, frequency_spectrum, xmin, xmax, vectors_matrix)
#transfer_vector = one_pass_mask(vmin, vmax, frequency_spectrum)
transfer_vector = one_doesnt_pass_mask(vmin, vmax, frequency_spectrum)
#transfer_vector = np.full(len(frequency_spectrum), 1)   # no mask, all rays pass

for i in range(len(frequency_spectrum)):
    v = frequency_spectrum[i]
    grating_matrix = grating(ψ, lambda0, v)
    free_space_matrix = free_space(f, v)
    lens = lens_matrix(f)

    fourier_plane_vector = vectors_matrix[:, i]
    after_fourier_vector = np.dot(free_space_matrix, fourier_plane_vector)
    lens_vector = np.dot(lens, after_fourier_vector)
    after_lens_vector = np.dot(free_space_matrix, lens_vector)
    grating_vector = np.dot(grating_matrix, after_lens_vector)
    after_grating_vector = np.dot(free_space_matrix, grating_vector)

    x_fourier = fourier_plane_vector[0]
    x_after_fourier = after_fourier_vector[0]
    x_after_lens = after_lens_vector[0]
    x_after_grating = after_grating_vector[0]

    if transfer_vector[i] == 1:    # plot only the vectors that pass the mask
        plt.plot([2*f, 3*f, 4*f], [x_fourier, x_after_fourier, x_after_lens], color=colors[i])

plt.title("Pulse Shaper: Rectangular Spatio - Temporal Ray Pulse")
plt.xlabel("z - optical axis [mm]")
plt.ylabel("x [mm]")
plt.grid()
plt.show()
