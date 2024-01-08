import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

def gaussian_function(x, mean, variance):
    return np.exp(-((x - mean) ** 2) / (2 * variance))

def tau_calculus():
    no_w = 1.4938
    ne_w = 1.4598
    L = 0.5 * 1e-2      # m
    c = 3.0e8          # m.s^-1

    result = no_w * ne_w * L / (2 * c * abs(no_w - ne_w))
    
    return round(result*1e9, 1) # ns

def correlation_coefficient(mean, variance, tau):
    # Define the range for integration
    integration_range = [-np.inf, np.inf]

    # Define the functions f and g
    f = lambda x: gaussian_function(x, mean, variance)
    g = lambda x: gaussian_function(x - tau, mean, variance)

    # Calculate the numerator [f * g](tau)
    numerator, _ = quad(lambda x: f(x) * g(x), *integration_range)

    # Calculate the denominator integral(f^2(t) dt)
    denominator, _ = quad(lambda x: f(x) ** 2, *integration_range)

    # Calculate the correlation coefficient
    correlation_coeff = numerator / denominator

    return correlation_coeff

mean = 0
variance = 1
tau_values = np.linspace(-3.5, 3.5, 100)
tau_m_value = tau_calculus()

intensity = [correlation_coefficient(mean, variance, tau-tau_m_value)**2 for tau in tau_values]

plt.plot(tau_values, intensity, color = 'r', label = r"I($\tau$)")
plt.axvline(tau_m_value, color = 'b', label = r"$\tau_m$", linestyle = "--")
plt.title("Photo-diode's intensity")
plt.xlabel(r"$\tau$")
plt.ylabel("Intensity")
plt.legend()

plt.show()
