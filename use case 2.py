import numpy as np
from functions import *
import matplotlib.pyplot as plt
from numpy import cos

c = 2.99 * (10 ** 11)  # def speed of light in mm/s

# set parameters of prisms system
M = -10
M2 = -10
D = 50000
L = 50
lambda_0 = 5e-4
v = c/lambda_0
f = 20
D2 = 200000
D3 = 50000

initial_vector = np.transpose(np.array([0, 0, 10, lambda_0]))
prism_1 = create_matrix(M, 0, 0, 1/M, 0, D, M*D/lambda_0, 0, 0)
prism_2 = create_matrix(1/M, 0, 0, M, 0, -M*D, -D/lambda_0, 0, 0)
prism_3 = create_matrix(M2, 0, 0, 1/M2, 0, D3, M2*D3/lambda_0, 0, 0)
lens_1 = lens_matrix(f)
lens_2 = lens_matrix(f)
prism_4 = create_matrix(M, 0, 0, 1/M, 0, D2, M*D2/lambda_0, 0, 0)
free_space_matrix = free_space(L, v)

prism_1_vector = np.dot(prism_1, initial_vector)
before_prism_2_vector = np.dot(free_space_matrix, prism_1_vector)
prism_2_vector = np.dot(prism_2, before_prism_2_vector)
before_prism_3_vector = np.dot(free_space_matrix, prism_2_vector)
prism_3_vector = np.dot(prism_3, before_prism_3_vector)
before_lens_1_vector = np.dot(free_space(5,v),prism_3_vector)
lens_1_vector = np.dot(lens_1,before_lens_1_vector)
before_lens_2_vector = np.dot(free_space(40,v),lens_1_vector)
lens_2_vector = np.dot(lens_2,before_lens_2_vector)
before_prism_4_vector = np.dot(free_space(5,v),lens_2_vector)
prism_4_vector = np.dot(prism_4,before_prism_4_vector)
final_vector = np.dot(free_space(-5,v),prism_4_vector)

plt.plot([0,20,L*cos(25)+20,L*cos(25)+20+L,L*cos(25)+20+L+50*cos(25), L*cos(25)+20+L+50*cos(25)+10*cos(180-102.5)]
         ,[initial_vector[0],prism_1_vector[0],prism_2_vector[0],before_prism_3_vector[0], before_prism_4_vector[0], -600], 'o-')

plt.title("Article Case 2")
plt.xlabel("z - optical axis [mm]")
plt.ylabel("x [mm]")
plt.grid()
plt.show()


# L*cos(25)+20+L+50*cos(25)+0.2*cos(102.5) , ,final_vector[0]]