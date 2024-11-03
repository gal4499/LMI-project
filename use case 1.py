import numpy as np
from functions import *
import matplotlib.pyplot as plt
from numpy import cos

c = 2.99 * (10 ** 11)  # def speed of light in mm/s

# set parameters of prisms system
M = -10
D = 50000
L = 50
lambda_0 = 5e-4
v = c/lambda_0

initial_vector = np.transpose(np.array([0, 0, 10, lambda_0]))
prism_1 = create_matrix(M, 0, 0, 1/M, 0, D, M*D/lambda_0, 0, 0)
prism_2 = create_matrix(1/M, 0, 0, M, 0, -M*D, -D/lambda_0, 0, 0)
prism_3 = create_matrix(M, 0, 0, 1/M, 0, -D, -M*D/lambda_0, 0, 0)
prism_4 = create_matrix(1/M, 0, 0, M, 0, M*D, D/lambda_0, 0, 0)
free_space_matrix = free_space(L, v)

prism_1_vector = np.dot(prism_1, initial_vector)
before_prism_2_vector = np.dot(free_space_matrix, prism_1_vector)
prism_2_vector = np.dot(prism_2, before_prism_2_vector)
before_prism_3_vector = np.dot(free_space_matrix, prism_2_vector)
prism_3_vector = np.dot(prism_3, before_prism_3_vector)
before_prism_4_vector = np.dot(free_space_matrix, prism_3_vector)
prism_4_vector = np.dot(prism_4, before_prism_4_vector)

plt.plot([0, 20, L*cos(25)+20, L*cos(25)+L+20, 2*L*cos(25)+L+20, 2*L*cos(25)+L+40], [initial_vector[0],prism_1_vector[0], prism_2_vector[0], before_prism_3_vector[0], before_prism_4_vector[0], prism_4_vector[0]], 'o-')

plt.title("Article Case 1")
plt.xlabel("z - optical axis [mm]")
plt.ylabel("x [mm]")
plt.grid()
plt.show()
