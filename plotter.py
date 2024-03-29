from collections import OrderedDict

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')


class Plotter:

    def __init__(self):
        plt.figure()

    def add_polygon(self, xs, ys):
        plt.fill(xs, ys, 'lightgray', label='Polygon')

    def add_point(self, x, y, kind=None):
        if kind == 'outside':
            plt.plot(x, y, 'ro', label='Outside')
        elif kind == 'boundary':
            plt.plot(x, y, 'bo', label='Boundary')
        elif kind == 'inside':
            plt.plot(x, y, 'go', label='Inside')
        else:
            plt.plot(x, y, 'ko', label='Unclassified')

    def add_line(self, x, y, name):
        """ Adds line to a plotter object """

        plt.plot(x, y, 'k', label=name)

    def add_label(self, x_axis, y_axis, title):
        """ Adds axis and title labels to a plotter object """

        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.title(title)

    def show(self):
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = OrderedDict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys())
        plt.show()

    def close(self):
        """ Clears plotter object """

        plt.clf()
