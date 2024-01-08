import sys
import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QDial, QLabel, QHBoxLayout, QPushButton

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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Correlation Factor GUI")

        # Example parameters
        self.mean = 0
        self.variance = 1
        self.tau_value = 0
        self.tau_m_value = tau_calculus()

        # Generate x values
        x_values = np.linspace(-5, 5, 1000)

        # Calculate y values for the Gaussian functions
        f_values = gaussian_function(x_values, self.mean, self.variance)
        g_values = gaussian_function(x_values - self.tau_value, self.mean, self.variance)

        self.figure, self.ax = plt.subplots()

        self.canvas = FigureCanvas(self.figure)

        # Tau Dial
        self.tau_dial = QDial()
        self.tau_dial.setMinimum(-35)
        self.tau_dial.setMaximum(35)
        self.tau_dial.valueChanged.connect(self.update_plot)
        self.tau_label = QLabel('𝜏: 0.0')

        # Push Button
        self.tau_button = QPushButton(r"Set 𝜏 at 0 -> 𝜏m value")
        self.tau_button.clicked.connect(self.set_tau_value)

        main_layout = QVBoxLayout()

        plot_layout = QVBoxLayout()
        plot_layout.addWidget(self.canvas)

        dial_layout = QHBoxLayout()
        dial_layout.addWidget(self.tau_dial)
        dial_layout.addWidget(self.tau_label)
        dial_layout.addWidget(self.tau_button)

        main_layout.addLayout(plot_layout)
        main_layout.addLayout(dial_layout)

        # Set the main layout for the widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.update_plot()

    def set_tau_value(self):
        self.tau_dial.setValue(0)
        self.update_plot()

    def update_plot(self):
        # Update QLabel values
        self.tau_value = self.tau_dial.value() / 10.0  # Adjust for finer control
        self.tau_label.setText(f'𝜏: {self.tau_value:.2f} ns')

        # Clear previous plot
        self.ax.cla()

        # Generate x values
        x_values = np.linspace(-5, 5, 1000)

        # Calculate y values for the Gaussian functions
        f_values = gaussian_function(x_values, self.mean, self.variance)
        g_values = gaussian_function(x_values - self.tau_value, self.mean, self.variance)  # Translate g by tau

        self.ax.plot(x_values, f_values, label='f(x)')
        self.ax.plot(x_values, g_values, label=r'g(x - ($\tau - \tau_m$))')

        # Calculate and display correlation coefficient
        correlation_coeff = correlation_coefficient(self.mean, self.variance, self.tau_value)
        correlation_coeff = round(correlation_coeff, 2)

        # Customize labels, limits, and title as needed
        self.ax.set_xlabel('time (ns)')
        self.ax.set_ylabel('value')
        self.ax.set_title(r'Overlap: $\gamma_{corr} =$'+ str(correlation_coeff))

        # Add legend
        self.ax.legend()

        # Trigger the canvas to update
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
