import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QSizePolicy


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig, self.axes = plt.subplots(figsize=(width, height), dpi=dpi)
        super(MplCanvas, self).__init__(self.fig)
        self.setParent(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.updateGeometry()

    def resizeEvent(self, event):
        super(MplCanvas, self).resizeEvent(event)
        self.adjust_plot_elements()

    def adjust_plot_elements(self):
        width, height = self.fig.get_size_inches() * self.fig.dpi
        scaling_factor = min(width, height) / 400
        self.axes.title.set_fontsize(12 * scaling_factor)
        self.axes.xaxis.label.set_fontsize(10 * scaling_factor)
        self.axes.yaxis.label.set_fontsize(10 * scaling_factor)
        self.axes.tick_params(axis='both', which='major', labelsize=8 * scaling_factor)

        if self.axes.get_legend():
            self.axes.legend(fontsize=8 * scaling_factor, loc=(1.01, 0.5))
        self.fig.tight_layout()
        self.draw()


class CycloidSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cycloid Trajectory Simulator")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.layout.addWidget(self.canvas)

        self.radius_label = QLabel("Радиус:")
        self.radius_input = QLineEdit()
        self.angular_acc_label = QLabel("Угловое ускорение:")
        self.angular_acc_input = QLineEdit()

        self.layout.addWidget(self.radius_label)
        self.layout.addWidget(self.radius_input)
        self.layout.addWidget(self.angular_acc_label)
        self.layout.addWidget(self.angular_acc_input)

        self.plot_button = QPushButton("Построить траекторию")
        self.plot_button.clicked.connect(self.start_animation)
        self.layout.addWidget(self.plot_button)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.time_elapsed = 0

        self.stop_timer = QTimer()
        self.stop_timer.setSingleShot(True)
        self.stop_timer.timeout.connect(self.stop_animation)

    def start_animation(self):
        self.time_elapsed = 0
        self.stop_timer.start(7000)
        self.timer.start(50)

    def update_plot(self):
        try:
            radius = float(self.radius_input.text())
            angular_acc = float(self.angular_acc_input.text())
            if radius <= 0:
                return
        except ValueError:
            return

        self.time_elapsed += 0.05

        speed = angular_acc * self.time_elapsed
        omega_w = speed / radius

        t = np.linspace(0, self.time_elapsed, 1000)
        x = radius * t * omega_w - radius * np.sin(omega_w * t)
        y = radius - radius * np.cos(omega_w * t)

        theta = np.linspace(0, 2 * np.pi, 100)
        circle_x = radius * np.cos(theta) + (radius * self.time_elapsed * omega_w)
        circle_y = radius * np.sin(theta) + radius

        self.canvas.axes.clear()
        self.canvas.axes.plot(x, y, label="Траектория точки", color='blue')
        self.canvas.axes.plot(circle_x, circle_y, 'r-', label="Вращающаяся окружность",
                              linewidth=4)

        self.canvas.axes.scatter(x[-1], y[-1], s=100, color='black', zorder=5,
                                 label="Текущая позиция")

        self.canvas.axes.set_xlabel("x")
        self.canvas.axes.set_ylabel("y")
        self.canvas.axes.axis('equal')
        self.canvas.axes.legend()
        self.canvas.axes.grid(True)
        self.canvas.draw()

    def stop_animation(self):
        self.timer.stop()
        print("Обновление графика остановлено")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CycloidSimulator()
    window.show()
    sys.exit(app.exec_())