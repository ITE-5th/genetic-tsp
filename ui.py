import os
import sys

import qdarkstyle
from PyQt5 import uic, QtWidgets

from tsp.city import City
from tsp.genetic_algorithm import GeneticAlgorithm
from tsp.path import Path

FormClass = uic.loadUiType("ui.ui")[0]


class Ui(QtWidgets.QMainWindow, FormClass):
    background_color = (255, 255, 255, 1)

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.current_path = Path([])
        self.plotWidget.setBackground(Ui.background_color)
        self.setup_events()

    def setup_events(self):
        self.solveButton.clicked.connect(self.solve)
        self.resetButton.clicked.connect(self.reset)
        self.addPointButton.clicked.connect(self.add_point)

    def solve(self):
        iterations, population_size, tournament_size, mutation_rate = self.iterationsSpinBox.value(), self.populationSizeSpinBox.value(), self.tournamentSizeSpinBox.value(), self.mutationRateSpinBox.value()
        ga = GeneticAlgorithm(self.path.path, population_size, mutation_rate, tournament_size)
        solution = ga.evolve_for(iterations)
        self.plot_path(solution)

    def plot_path(self, path, scatter=False):
        xs, ys = path.to_numpy_array()
        self.plotWidget.plot(xs, ys, pen='r', clear=True, scatter=scatter)

    def reset(self):
        self.current_path.reset()
        self.plot_path(self.current_path)

    def add_point(self):
        x, y = self.pointXSpinBox.value(), self.pointXSpinBox.value()
        self.current_path.add_city(City(x, y))
        self.plot_path(self.current_path, scatter=True)


if __name__ == '__main__':
    os.environ['PYQTGRAPH_QT_LIB'] = "PyQt5"
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet(qdarkstyle.load_stylesheet_from_environment(is_pyqtgraph=True))
    ui = Ui()
    ui.setWindowTitle("Image Segmentation")
    ui.show()
    app.exec_()
