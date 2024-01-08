import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QDial, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np

class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)

        # Constants
        self.no_1064nm = 1.4938
        self.ne_1064nm = 1.4598
        self.no_SHG = 1.5124
        self.ne_SHG = 1.4704

        # Initialize instance variables for coordinates
        self.x_end = 0.0
        self.y_end = 0.0
        self.z_end = 0.0

        # Create a Matplotlib figure and axes
        self.figure = plt.figure()
        self.ax = self.figure.add_subplot(111, projection='3d')

        # Embed the Matplotlib plot in the PyQt widget
        self.canvas = FigureCanvas(self.figure)

        # Create QDials for phi and theta
        self.phi_dial = QDial()
        self.theta_dial = QDial()

        # Set the range for phi dial from 0 to 2*pi and for theta from 0 to pi
        self.phi_dial.setMinimum(0)
        self.phi_dial.setMaximum(360)
        self.theta_dial.setMinimum(0)
        self.theta_dial.setMaximum(180)

        # Connect dial signals to update the plot
        self.phi_dial.valueChanged.connect(self.update_plot)
        self.theta_dial.valueChanged.connect(self.update_plot)

        # Create QLabel widgets for displaying phi and theta values
        self.phi_label = QLabel('Phi: 0.0')
        self.theta_label = QLabel('Theta: 0.0')

        # Create layouts
        main_layout = QVBoxLayout()

        plot_layout = QVBoxLayout()
        plot_layout.addWidget(self.canvas)

        dial_layout = QHBoxLayout()
        dial_layout.addWidget(self.phi_dial)
        dial_layout.addWidget(self.phi_label)
        dial_layout.addWidget(self.theta_dial)
        dial_layout.addWidget(self.theta_label)

        main_layout.addLayout(plot_layout)
        main_layout.addLayout(dial_layout)

        # Set the main layout for the widget
        self.setLayout(main_layout)

        # Initial phi and theta values
        self.phi_value = np.pi / 4
        self.theta_value = np.pi / 4

        # Plot the 3D indicatrix
        self.update_plot()

    def plot_ellipse(self, a, b, c, color, alpha, label):
        u = np.linspace(0, 2 * np.pi, 200)
        v = np.linspace(0, np.pi, 100)
        x = a * np.outer(np.cos(u), np.sin(v))
        y = b * np.outer(np.sin(u), np.sin(v))
        z = c * np.outer(np.ones(np.size(u)), np.cos(v))
        self.ax.plot_surface(x, y, z, color='b', alpha=0.6, label='Indices surface')

    def draw_line(self, a, b, c, phi, theta, label = None):
        # Calculate the coordinates of the endpoint of the line on the ellipse
        self.x_end = a * np.cos(phi) * np.sin(theta)
        self.y_end = b * np.sin(phi) * np.sin(theta)
        self.z_end = c * np.cos(theta)

        # Plot the line
        self.ax.plot([0, self.x_end], [0, self.y_end], [0, self.z_end], color='r', label=label)

    def update_plot(self):
        # Update phi and theta values
        self.phi_value = np.deg2rad(self.phi_dial.value())
        self.theta_value = np.deg2rad(self.theta_dial.value())

        # Update QLabel values
        self.phi_label.setText(f'Phi: {np.rad2deg(self.phi_value):.2f}°')
        self.theta_label.setText(f'Theta: {np.rad2deg(self.theta_value):.2f}°')

        # Clear previous plot
        self.ax.cla()

        # Plot outer ellipse
        self.plot_ellipse(self.ne_SHG, self.ne_SHG, self.no_SHG, 'b', 0.1, r'$n$ (SHG)')

        # Draw the line
        self.draw_line(self.ne_SHG, self.ne_SHG, self.no_SHG, self.phi_value, self.theta_value)

        # Update coordinates label
        coordinates_text = f'Coordinates: (X:{self.x_end:.2f}, Y:{self.y_end:.2f}, Z:{self.z_end:.2f})'

        # Customize labels, limits, and title as needed
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_xlim([-2, 2])
        self.ax.set_ylim([-2, 2])
        self.ax.set_zlim([-2, 2])
        self.ax.set_title(coordinates_text)

        # Add legend
        self.ax.legend()

        # Trigger the canvas to update
        self.canvas.draw()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Create the Matplotlib widget
        self.matplotlib_widget = MatplotlibWidget(self)

        # Set the central widget
        self.setCentralWidget(self.matplotlib_widget)

        # Set window properties
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Non-Linear Optics')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
