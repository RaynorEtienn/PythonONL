import numpy as np
import matplotlib.pyplot as plt

# Given refractive indices
no_w = 1.4938
ne_w = 1.4598
no_2w = 1.5124
ne_2w = 1.4704

# Given parameters
lambda_w = 1064e-9  # Wavelength for fundamental wave in meters
lambda_2w = 532e-9  # Wavelength for second harmonic wave in meters

# Function to calculate epsilon for the fundamental wave
def epsilon_w(x0, y0, z0, delta_z):
    alpha = 10.132  # Non-collinear angle for phase matching in degrees
    chi2 = -1.17e-8  # Effective nonlinear coefficient for non-collinear generation

    # Convert angles to radians
    alpha_rad = np.radians(alpha)

    # Equation for epsilon_w
    result = (
        (no_w * ne_w) * (x0**2 + y0**2) +
        delta_z * np.tan(alpha_rad) * (x0**2 + y0**2) -
        delta_z * (4j * chi2 * np.pi * lambda_w**2) / (3e8**2 * 2 * np.pi / lambda_w * np.cos(alpha_rad)) * np.exp(
            -1j * (2 * np.pi / lambda_w) * z0) * (no_w * ne_2w)
    )

    return result

# Function to calculate epsilon for the second harmonic wave
def epsilon_2w(x0, y0, z0, delta_z):
    alpha_collinear = 41.3  # Collinear angle for phase matching in degrees
    chi2_collinear = -7.95e-9  # Effective nonlinear coefficient for collinear generation

    # Convert angles to radians
    alpha_collinear_rad = np.radians(alpha_collinear)

    # Equation for epsilon_2w
    result = (
        (no_2w * ne_2w) * (x0**2 + y0**2) -
        delta_z * (16j * chi2_collinear * np.pi * lambda_w**2) / (3e8**2 * 2 * np.pi / lambda_2w) * np.exp(
            1j * (2 * np.pi / lambda_2w) * z0) * (no_w * ne_w)
    )

    return result

# Function to calculate intensity and phase of SHG
def shg_intensity_phase(epsilon_2w_values):
    intensity = np.abs(epsilon_2w_values)**2
    phase = np.angle(epsilon_2w_values)

    return intensity, phase

# Example values for x0, y0, and delta_z
x0_values = np.linspace(-1, 1, 100)
y0_values = np.linspace(-1, 1, 100)
delta_z_values = np.linspace(0, 1, 100)

# Create a meshgrid for x0, y0, and delta_z
x0_mesh, y0_mesh, delta_z_mesh = np.meshgrid(x0_values, y0_values, delta_z_values, indexing='ij')

# Different z values
z_values = [0, 0.1, 0.2]

# Plot the results for different z values
fig, axs = plt.subplots(len(z_values), 2, figsize=(12, 6 * len(z_values)), sharex=True)

for i, z_value in enumerate(z_values):
    epsilon_2w_values = epsilon_2w(x0_mesh, y0_mesh, z_value, delta_z_mesh)  # Calculate epsilon_2w for the given z value
    shg_intensity, shg_phase = shg_intensity_phase(epsilon_2w_values)

    axs[i, 0].contourf(x0_mesh[:, :, 0], y0_mesh[:, :, 0], shg_intensity[:, :, 0], cmap='viridis')
    axs[i, 0].set_title(f'Intensity of SHG at z={z_value}')

    axs[i, 1].contourf(x0_mesh[:, :, 0], y0_mesh[:, :, 0], shg_phase[:, :, 0], cmap='hsv')
    axs[i, 1].set_title(f'Phase of SHG at z={z_value}')

plt.xlabel('x0')
plt.ylabel('y0')
plt.show()
