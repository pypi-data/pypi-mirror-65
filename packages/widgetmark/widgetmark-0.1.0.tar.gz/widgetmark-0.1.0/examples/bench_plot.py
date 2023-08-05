import widgetmark
import numpy as np


class ZoomingLineGraph(widgetmark.UseCase):

    backend = widgetmark.GuiBackend.QT
    goal = 30.0
    minimum = 20.0
    tolerance = 0.05
    repeat = 100
    parameters = {"plot_lib": list(widgetmark.PlottingLibraryEnum)}

    def setup_widget(self):
        self._plot = widgetmark.AbstractBasePlot.using(self.plot_lib)
        curve = self._plot.add_item(item_type=widgetmark.DataItemType.CURVE)
        x = np.linspace(-2, 2, 10000)
        y = np.random.randint(-2, 2, 10000)
        curve.set_data(np.array([x, y]))
        self._plot.set_range(view_range=((-2, 2), (-2, 2)))
        return self._plot

    def operate(self):
        self._plot.set_range(
            view_range=[[e * 1.05 for e in r] for r in self._plot.get_range()])


class RandomLineGraph(widgetmark.UseCase):

    backend = widgetmark.GuiBackend.QT
    goal = 30.0
    minimum = 20.0
    tolerance = 0.05
    repeat = 100
    timeout = 20
    parameters = {
        "plot_lib": list(widgetmark.PlottingLibraryEnum),
        "size": [100, 10000, 100000],
    }

    def setup_widget(self):
        self._plot = widgetmark.AbstractBasePlot.using(self.plot_lib)
        self._curve = self._plot.add_item(
            item_type=widgetmark.DataItemType.CURVE)
        self._curve.set_data(np.array([[0.0, 1.0], [0.0, 1.0]]))
        self._plot.set_range(view_range=((0, self.size), (0, 100)))
        return self._plot

    def operate(self):
        self._curve.set_data(np.array([
            np.arange(0, self.size),
            np.random.randint(0, 100, self.size),
        ]))
