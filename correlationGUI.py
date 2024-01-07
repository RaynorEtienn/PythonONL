import sys
import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QDial, QLabel, QHBoxLayout

def gaussian_function(x, mean, variance):
    return np.exp(-((x - mean) ** 2) / (2 * variance))

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

        # Generate x values
        x_values = np.linspace(-5, 5, 1000)

        # Calculate y values for the Gaussian functions
        f_values = gaussian_function(x_values, self.mean, self.variance)
        g_values = gaussian_function(x_values - self.tau_value, self.mean, self.variance)

        self.figure, self.ax = plt.subplots()

        self.canvas = FigureCanvas(self.figure)

        # Test Tau
        self.tau_dial = QDial()
        self.tau_dial.setMinimum(-35)
        self.tau_dial.setMaximum(35)
        self.tau_dial.valueChanged.connect(self.update_plot)
        self.tau_label = QLabel('Tau: 0.0')

        main_layout = QVBoxLayout()

        plot_layout = QVBoxLayout()
        plot_layout.addWidget(self.canvas)

        dial_layout = QHBoxLayout()
        dial_layout.addWidget(self.tau_dial)
        dial_layout.addWidget(self.tau_label)

        main_layout.addLayout(plot_layout)
        main_layout.addLayout(dial_layout)

        # Set the main layout for the widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.update_plot()

    def update_plot(self):
        # Update QLabel values
        self.tau_value = self.tau_dial.value() / 10.0  # Adjust for finer control
        self.tau_label.setText(f'Tau: {self.tau_value:.2f}')

        # Clear previous plot
        self.ax.cla()

        # Generate x values
        x_values = np.linspace(-5, 5, 1000)

        # Calculate y values for the Gaussian functions
        f_values = gaussian_function(x_values, self.mean, self.variance)
        g_values = gaussian_function(x_values - self.tau_value, self.mean, self.variance)  # Translate g by tau

        self.ax.plot(x_values, f_values, label='f(x)')
        self.ax.plot(x_values, g_values, label=f'g(x - {self.tau_value})')

        # Calculate and display correlation coefficient
        correlation_coeff = correlation_coefficient(self.mean, self.variance, self.tau_value)
        correlation_coeff = round(correlation_coeff, 2)

        # Customize labels, limits, and title as needed
        self.ax.set_xlabel('time')
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
