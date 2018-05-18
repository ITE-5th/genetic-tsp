import os
import sys

import pyqtgraph as pg
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
        self.plotWidget.setXRange(0, 100)
        self.plotWidget.setYRange(0, 100)
        self.setup_events()

    def setup_events(self):
        self.solveButton.clicked.connect(self.solve)
        self.resetButton.clicked.connect(self.reset)
        self.addPointButton.clicked.connect(self.add_point)

    def solve(self):
        iterations, population_size, tournament_size, mutation_rate = self.iterationsSpinBox.value(), self.populationSizeSpinBox.value(), self.tournamentSizeSpinBox.value(), self.mutationRateSpinBox.value()
        ga = GeneticAlgorithm(self.current_path.path, population_size, mutation_rate, tournament_size)
        solution = ga.evolve_for(iterations)
        self.plot_path(solution)

    def plot_path(self, path, just_scatter=False):
        xs, ys = path.to_numpy_array()
        if not just_scatter:
            self.plotWidget.plot(xs, ys, pen=pg.mkPen(color=(200, 200, 255), width=2), clear=True)
        else:
            s1 = pg.ScatterPlotItem(xs, ys, size=7, pen=pg.mkPen(None), brush=pg.mkBrush(255, 255, 255, 120))
            self.plotWidget.addItem(s1)

    def reset(self):
        self.current_path.reset()
        self.plot_path(self.current_path)

    def add_point(self):
        x, y = self.pointXSpinBox.value(), self.pointYSpinBox.value()
        self.current_path.add_city(City(x, y))
        self.plot_path(self.current_path, True)


if __name__ == '__main__':
    os.environ['PYQTGRAPH_QT_LIB'] = "PyQt5"
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui()
    ui.setWindowTitle("Genetic TSP")
    ui.show()
    app.exec_()
