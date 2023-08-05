from qtpy import QtWidgets
import pytest
import widgetmark


@pytest.mark.parametrize("lib", [
    (widgetmark.PlottingLibraryEnum.PYQTGRAPH, widgetmark.PyQtGraphPlot),
    (widgetmark.PlottingLibraryEnum.MATPLOTLIB, widgetmark.MatPlotLibPlot),
])
def test_abstract_base_plot_factory(qtbot, lib):
    window = QtWidgets.QMainWindow()
    plot = widgetmark.AbstractBasePlot.using(lib[0])
    window.setCentralWidget(plot)
    qtbot.addWidget(window)
    assert isinstance(plot, lib[1])


@pytest.mark.parametrize("lib", list(widgetmark.PlottingLibraryEnum))
@pytest.mark.parametrize("data_item", list(widgetmark.DataItemType))
def test_abstract_base_plot_add_item(qtbot, lib, data_item):
    window = QtWidgets.QMainWindow()
    plot = widgetmark.AbstractBasePlot.using(lib)
    window.setCentralWidget(plot)
    qtbot.addWidget(window)
    item = plot.add_item(item_type=data_item)
    assert isinstance(item._item, plot.item_type_mapping.get(data_item)[0])
