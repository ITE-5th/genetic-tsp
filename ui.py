import copy
import os
import sys
import time

import pyqtgraph as pg
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QApplication, QGraphicsPixmapItem
from qtconsole.qt import QtGui

from misc.cities_reader import CitiesReader
from tsp.city import City
from tsp.genetic_algorithm import GeneticAlgorithm
from tsp.path import Path

os.environ['PYQTGRAPH_QT_LIB'] = "PyQt5"
FormClass = uic.loadUiType("ui.ui")[0]


class Ui(QtWidgets.QMainWindow, FormClass):
    background_color = (255, 255, 255, 1)
    max_range = 100
    incremental = True
    time_between_plot = 0.1

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.current_path = Path([])
        self.plotWidget.setBackground(Ui.background_color)
        self.plotWidget.setXRange(0, Ui.max_range)
        self.plotWidget.setYRange(0, Ui.max_range)
        self.pixel_map = QtGui.QPixmap("city.png")
        self.image_scale = 0.1

        self.setup_events()

    def handle_item_clicked(self, event):
        pos = self.plotWidget.mapToView(event.pos())
        x, y = pos.x(), pos.y()
        self.current_path.add_city(City(x, y))
        self.plot_path(self.current_path, True)

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
        self.loadButton.clicked.connect(self.load)
        self.plotWidget.mouseReleaseEvent = self.handle_item_clicked

    def solve(self):
        if len(self.current_path.path) == 0:
            return
        iterations, population_size, tournament_size, mutation_rate = self.iterationsSpinBox.value(), self.populationSizeSpinBox.value(), self.tournamentSizeSpinBox.value(), self.mutationRateSpinBox.value()
        ga = GeneticAlgorithm(self.current_path.path, population_size, mutation_rate, tournament_size)
        if not Ui.incremental:
            solution = ga.evolve(iterations)
            self.show_solution(solution)
        else:
            it = ga.evolve_incrementally(iterations)
            for solution in it:
                self.show_solution(solution)
                time.sleep(Ui.time_between_plot)
            print("finished")

    def show_solution(self, solution):
        temp = copy.deepcopy(solution)
        temp.add_city(solution[0])
        self.plot_path(temp)
        self.plot_path(temp, True)
        self.distanceLabel.setText(str(round(temp.distance(), 3)))
        QApplication.processEvents()

    def plot_path(self, path, just_scatter=False):
        xs, ys = path.to_numpy_array()
        if not just_scatter:
            self.plotWidget.plot(xs, ys, pen=pg.mkPen(color=(255, 255, 255), width=2), clear=True)
        else:
            for i in range(len(xs)):
                image = QGraphicsPixmapItem(self.pixel_map)
                image.scale(self.image_scale, -self.image_scale)
                image.setPos(xs[i] - self.pixel_map.width() * self.image_scale / 2, ys[i] + self.pixel_map.height() * self.image_scale / 2)
                self.plotWidget.addItem(image)

    def reset(self):
        self.current_path.reset()
        self.plot_path(self.current_path)

    def add_point(self):
        x, y = self.pointXSpinBox.value(), self.pointYSpinBox.value()
        self.current_path.add_city(City(x, y))
        self.plot_path(self.current_path, True)

    def load(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, 'Choose A File')
            cities = CitiesReader.read(file_path, scaling_factor=0.01)
            self.current_path.set_path(cities)
            self.plot_path(self.current_path, just_scatter=True)
        except:
            pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui()
    ui.setWindowTitle("Genetic TSP")
    ui.show()
    app.exec_()
