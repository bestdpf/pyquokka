import sys
from PyQt4 import QtGui

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import matplotlib.pyplot as plt

import random

from quokka.sim.event import *


"""
this code is originally from stackoverflow
"""

class Window(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setWindowTitle('QuokkaVis')

        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.algLabel = QtGui.QLabel('Algorithm:')
        self.algList = QtGui.QComboBox()
        self.algList.addItems(['quokka', 'flb', 'ff'])
        self.topoLabel = QtGui.QLabel('Topology:')
        self.topoList = QtGui.QComboBox()
        self.topoList.addItems(['fattree','cernet','carnet','as2194'])
        # Just some button connected to `plot` method
        self.button = QtGui.QPushButton('Plot')
        self.button.clicked.connect(self.plot)



        # set the layout
        layout = QtGui.QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(self.toolbar,1,0,1,10)
        layout.addWidget(self.canvas,2,0,10,10)
        layout.addWidget(self.algLabel,13,0)
        layout.addWidget(self.algList,13,1)
        layout.addWidget(self.topoLabel,14,0)
        layout.addWidget(self.topoList,14,1)
        layout.addWidget(self.button,15,0)
        self.setLayout(layout)

    def plot(self):
        event = Event(self.algList.currentText(), self.topoList.currentText())
        pla,mdp = event.run()
        maxDelay = 0
        for flow, path, dis in mdp:
            dis = int(dis)
            if maxDelay < dis:
                maxDelay = dis
        if maxDelay > 500:
            maxDelay = 500

        xdata = range(0,maxDelay)
        ydata = maxDelay*[0.0]
        for flow, path, dis in mdp:
            dis = int(dis)
            if dis >= maxDelay:
                ydata[maxDelay -1 ] += 1
            else:
                ydata[dis] += 1
        for i in range(1,maxDelay):
            ydata[i] += ydata[i-1]
        for i in range(0,maxDelay):
            ydata[i] /= ydata[maxDelay - 1]

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.hold(False)

        # plot data
        ax.plot(xdata,ydata, 'r*-', )
    
        ax.set_xlabel('latency/ms')
        ax.set_ylabel('cdf')

        # refresh canvas
        self.canvas.draw()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())
