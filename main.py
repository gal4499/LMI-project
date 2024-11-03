#main final final final
import numpy as np
from functions import *
import tkinter as tk
from tkinter import simpledialog, messagebox
from sympy import sympify, symbols

omega = symbols('omega', real=True, positive=True)


def user_input(root):
    choice = simpledialog.askstring("Matrix Selection",
                                    "Enter the index of the next matrix:\n"
                                    "1. Lens \n"
                                    "2. Dispersive Slab \n"
                                    "3. Littrow Prism \n"
                                    "4. Prism \n"
                                    "5. Grating \n"
                                    "6. General Prism \n"
                                    "7. Curved Mirror \n",
                                    parent=root)
    return choice


def format_complex_number(number):
    #Format a complex number to hide the imaginary part if it's zero.
    if np.isclose(number.imag, 0):
        return f"{number.real:.6e}"
    return f"{number.real:.6e}{number.imag:+.6e}j"


def format_matrix(matrix):
    #Format a matrix to hide the imaginary part of complex numbers if it's zero.
    return "\n".join(["\t".join([format_complex_number(cell) for cell in row]) for row in matrix])


def check_non_physical(final_vector):
    #Check if the final vector has any pure imaginary values.
    for value in final_vector:
        if np.isclose(value.real, 0) and not np.isclose(value.imag, 0):
            return True
    return False


def main():
    root = tk.Tk()
    root.withdraw()  # Hide the root window as it's not needed for input
    root.update()  # Update the root window to ensure it's initialized

    # Create the matrix list window
    matrix_list_window = tk.Toplevel(root)
    matrix_list_window.geometry("300x200")
    matrix_list_window.title("Available Matrices")

    matrix_list_label = tk.Label(matrix_list_window, text="Available matrices:\n"
                                                          "1. Lens \n"
                                                          "2. Dispersive Slab \n"
                                                          "3. Littrow Prism \n"
                                                          "4. Prism \n"
                                                          "5. Grating \n"
                                                          "6. General Prism \n"
                                                          "7. Curved Mirror \n",
                                 font='50', justify='left')
    matrix_list_label.pack()

    initial_vector_str = simpledialog.askstring('Initial Vector',
                                                "Enter the initial vector, of the form: x, θ, t, f \n"
                                                "Units are mm, degrees, s, Hz",
                                                parent=root)  # Ensure dialogs have the root as parent

    if initial_vector_str:
        initial_vector = np.array([float(i) for i in initial_vector_str.split(',')])
        v = initial_vector[3]
        system_matrices = []
        matrices_indices = []
        count = 1

        while True:
            if count > 1:
                d = simpledialog.askfloat('Free Space',
                                          'Enter distance between previous and current optical component in mm \n'
                                          '(i.e. free space propagation distance)\n',
                                          parent=root)
                chosen_matrix = '0'
                mat = free_space(d, v)
                system_matrices.append(mat)
                matrices_indices.append(chosen_matrix)

            chosen_matrix = user_input(root)

            if chosen_matrix == '1':
                f = simpledialog.askfloat('Lens', "Enter focal length of the lens (in mm): ", parent=root)
                matrix = lens_matrix(f)
                messagebox.showinfo("New Component", "Matrix added: Lens", parent=root)

            elif chosen_matrix == '2':
                L = simpledialog.askfloat('Slab', 'Enter slab thickness (in mm)', parent=root)
                n = sympify(simpledialog.askstring('Dispersion',
                                                   "Enter n (refractive index) as a function of w (angular frequency). \n"
                                                   "For example, type: w**3 + 2*w + 1 ", parent=root))
                matrix = dispersive_slab_matrix(L, n, v)
                messagebox.showinfo("New Component", "Matrix added: Dispersive Slab", parent=root)

            elif chosen_matrix == '3':

                a = simpledialog.askfloat('a', "Enter the value for a: ", parent=root)
                b = simpledialog.askfloat('b', "Enter the value for b: ", parent=root)
                c = simpledialog.askfloat('c', "Enter the value for c: ", parent=root)
                d = simpledialog.askfloat('d', "Enter the value for d: ", parent=root)
                e = simpledialog.askfloat('e', "Enter the value for e: ", parent=root)
                f = simpledialog.askfloat('f', "Enter the value for f: ", parent=root)
                n_func = construct_refractive_index(a, b, c, d, e, f)
                ψ = (180 / np.pi) * simpledialog.askfloat('Prism Apex Angle', 'Enter prism apex angle in degrees',
                                                          parent=root)
                matrix = littrow_prism(ψ, n_func, v)
                messagebox.showinfo("New Component", "Matrix added: Littrow Prism", parent=root)

            elif chosen_matrix == '4':

                a = simpledialog.askfloat('a', "Enter the value for a: ", parent=root)
                b = simpledialog.askfloat('b', "Enter the value for b: ", parent=root)
                c = simpledialog.askfloat('c', "Enter the value for c: ", parent=root)
                d = simpledialog.askfloat('d', "Enter the value for d: ", parent=root)
                e = simpledialog.askfloat('e', "Enter the value for e: ", parent=root)
                f = simpledialog.askfloat('f', "Enter the value for f: ", parent=root)
                n_func = construct_refractive_index(a, b, c, d, e, f)
                ψ = (180 / np.pi) * simpledialog.askfloat('Prism Apex Angle', 'Enter prism apex angle in degrees',
                                                          parent=root)
                matrix = prism(ψ, n_func, v)
                messagebox.showinfo("New Component", "Matrix added: Prism", parent=root)

            elif chosen_matrix == '5':
                Λ = simpledialog.askfloat('Grating Period', 'Enter grating period (mm)', parent=root)
                ψ = (180 / np.pi) * simpledialog.askfloat('Incident Angle',
                                                          'Enter angle of incident ray to grating surface (not the normal!) in degrees',
                                                          parent=root)
                matrix = grating(ψ, Λ, v)
                messagebox.showinfo("New Component", "Matrix added: Grating", parent=root)

            elif chosen_matrix == '6':

                a = simpledialog.askfloat('a', "Enter the value for a: ", parent=root)
                b = simpledialog.askfloat('b', "Enter the value for b: ", parent=root)
                c = simpledialog.askfloat('c', "Enter the value for c: ", parent=root)
                d = simpledialog.askfloat('d', "Enter the value for d: ", parent=root)
                e = simpledialog.askfloat('e', "Enter the value for e: ", parent=root)
                f = simpledialog.askfloat('f', "Enter the value for f: ", parent=root)
                n_func = construct_refractive_index(a, b, c, d, e, f)
                ψ = (180 / np.pi) * simpledialog.askfloat('Prism Apex Angle', 'Enter prism apex angle in degrees',
                                                          parent=root)
                α = (180 / np.pi) * simpledialog.askfloat('Prism Apex Angle', 'Enter prism apex angle in degrees',
                                                          parent=root)
                θ = (180 / np.pi) * simpledialog.askfloat('Prism Orientation',
                                                          'Enter prism orientation towards optical path - \n'
                                                          'incident angle to prism normal, in degrees', parent=root)
                d = simpledialog.askfloat('Distance', 'Enter the distance between point of incidence to apex vertex, in mm',
                                          parent=root)
                matrix = general_prism(a, b, c, d, e, f, α, θ, d, v)
                messagebox.showinfo("New Component", "Matrix added: General Prism", parent=root)

            elif chosen_matrix == '7':
                R = simpledialog.askfloat('Curved Mirror', "Enter curvature radius of the mirror (in mm): ",
                                          parent=root)
                matrix = lens_matrix(R / 2)
                messagebox.showinfo("New Component", "Matrix added: Curved Mirror", parent=root)

            else:
                messagebox.showerror("Invalid choice. Please try again", parent=root)
                continue

            system_matrices.append(matrix)
            matrices_indices.append(chosen_matrix)
            count += 1
            done_or_not = messagebox.askyesno('', 'Are you done building the system?', parent=root)
            if done_or_not:
                break

        # Multiply all matrices to get the final system matrix
        final_matrix = np.eye(4, dtype=complex)  # Start with the identity matrix
        for mtrx in system_matrices:
            final_matrix = np.dot(mtrx, final_matrix)

        # Calculate the final vector
        final_vector = np.dot(final_matrix, initial_vector)

        # Print results
        result_window = tk.Tk()
        result_window.geometry("600x100")

        final_mat = tk.Label(result_window, text="Final system matrix and final vector are printed in the terminal",
                             font='50',
                             justify='left')
        final_mat.pack()
        print("Final System Matrix:\n", format_matrix(final_matrix))
        print("Final Vector:\n", [format_complex_number(x) for x in final_vector])

        # Check for non-physical output
        if check_non_physical(final_vector):
            messagebox.showwarning("Non-Physical Output",
                                   "The combination of values you entered generated a non-physical output vector")

        result_window.mainloop()

        # Close all windows
        matrix_list_window.destroy()
        result_window.destroy()
        root.quit()  # Terminate the Tkinter event loop
        root.destroy()  # Destroy the root window


if __name__ == "__main__":
    main()
