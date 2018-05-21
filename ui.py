import os
import sys

import pyqtgraph as pg
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QFileDialog

from misc.cities_reader import CitiesReader
from tsp.city import City
from tsp.genetic_algorithm import GeneticAlgorithm
from tsp.path import Path

os.environ['PYQTGRAPH_QT_LIB'] = "PyQt5"
FormClass = uic.loadUiType("ui.ui")[0]


class Ui(QtWidgets.QMainWindow, FormClass):
    background_color = (255, 255, 255, 1)
    max_range = 100

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.current_path = Path([])
        self.plotWidget.setBackground(Ui.background_color)
        self.plotWidget.setXRange(0, Ui.max_range)
        self.plotWidget.setYRange(0, Ui.max_range)
        self.setup_events()

    def setup_events(self):
        maxi = 10000
        self.iterationsSpinBox.setMaximum(maxi)
        self.populationSizeSpinBox.setMaximum(maxi)
        self.tournamentSizeSpinBox.setMaximum(maxi)
        self.mutationRateSpinBox.setMaximum(1)
        self.solveButton.clicked.connect(self.solve)
        self.resetButton.clicked.connect(self.reset)
        self.addPointButton.clicked.connect(self.add_point)
        self.loadButton.clicked.connect(self.load)

    def solve(self):
        if len(self.current_path.path) == 0:
            return
        iterations, population_size, tournament_size, mutation_rate = self.iterationsSpinBox.value(), self.populationSizeSpinBox.value(), self.tournamentSizeSpinBox.value(), self.mutationRateSpinBox.value()
        ga = GeneticAlgorithm(self.current_path.path, population_size, mutation_rate, tournament_size)
        solution = ga.evolve(iterations)
        solution.add_city(solution.path[0])
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

    def load(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Choose A File')
        cities = CitiesReader.read(file_path, scaling_factor=0.01)
        self.current_path.set_path(cities)
        self.plot_path(self.current_path, just_scatter=True)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui()
    ui.setWindowTitle("Genetic TSP")
    ui.show()
    app.exec_()
