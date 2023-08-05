from abc import abstractmethod, ABCMeta
from enum import Enum
from typing import Tuple, Dict, List, Type, Union, Sequence, Any
import logging

from qtpy import QtWidgets
import numpy as np
import pyqtgraph as pg
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.lines import Line2D

from .util import make_qt_abc_meta

logger = logging.getLogger(__name__)


class DataItemType(Enum):

    """
    Enumeration for different types of data visualization items
    which can be part of a plot.
    """

    CURVE = 0
    SCATTER = 1


class PlottingLibraryEnum(Enum):

    """
    Enumeration for different libraries which are supported by
    the
    """

    PYQTGRAPH = 0
    MATPLOTLIB = 1


class AbstractBasePlot(
    QtWidgets.QWidget,
    metaclass=make_qt_abc_meta(QtWidgets.QWidget),  # type: ignore
):

    """
    To write reusable use cases for different graph libraries,
    we will have to create a unified interface, which can then
    be implemented using different real graph libraries.
    """

    library: PlottingLibraryEnum = None  # type: ignore
    item_type_mapping: Dict[DataItemType, Tuple[Type, Dict]] = {}

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

    @classmethod
    def using(cls: Type["AbstractBasePlot"],
              library: PlottingLibraryEnum) -> "AbstractBasePlot":
        """
        Instantiate a plot instance from the given plotting library.

        Args:
            library: Library that is supposed to be used.
        """
        return cls.get_subclass_for_lib(library=library)()

    @classmethod
    def get_subclass_for_lib(
            cls: Type["AbstractBasePlot"],
            library: Union[PlottingLibraryEnum, str],
    ) -> Type["AbstractBasePlot"]:
        """
        Get a fitting implementation of the AbstractBasePlot which
        is based on the passed library name.

        Args:
            library: Library which should be used to create the plot

        Returns:
            Plot instance created using the passed library
        """
        fitting_classes: List[Type[AbstractBasePlot]] = [
            c for c in AbstractBasePlot.all_subclasses(cls)
            if library == c.library and c.library is not None
        ]
        if not fitting_classes:
            raise ValueError(f"No fitting subclass was found for the "
                             f"plot library {library}.")
        elif len(fitting_classes) > 1:
            logger.debug(f"Multiple subclasses were found for the "
                         f"plot library {library}.")
        return fitting_classes[0]

    @staticmethod
    def all_subclasses(cls):
        """Search for all subclasses of a class recursively."""
        return set(cls.__subclasses__()).union([
            s for c in cls.__subclasses__()
            for s in AbstractBasePlot.all_subclasses(c)
        ])

    @abstractmethod
    def add_item(self, item_type: DataItemType) -> "AbstractDataItem":
        """
        Add an item based on the passed type to the plot.

        Args:
            item_type: What type of item is supposed to be added to the plot

        Returns:
            Item which was added to the
        """
        pass

    @abstractmethod
    def set_range(self,
                  view_range: Sequence[Sequence[float]]) -> None:
        """
        Set the plots visible range in x and y direction.

        Args:
            view_range: Visible range of the plot
                        ((x_min, x_max), (y_min, y_max))
        """
        pass

    @abstractmethod
    def get_range(self) -> Sequence[Sequence[float]]:
        """
        Get the plots current view range of both axes as
        ((x_min, x_max), (y_min, y_max)).

        Returns:
            Current View Range for the X and Y axis
        """
        pass


class AbstractDataItem(metaclass=ABCMeta):

    def __init__(self, data_item: Any):
        """
        Wrapper for any sort of data item for a plot. This data item can be
        bargraphs, curves, scatterplots and more.

        Args:
            data_item: Data Item that should be wrapped and which's data should
                       be manipulated
        """
        self._item: Any = data_item  # type: ignore

    @abstractmethod
    def get_data(self) -> np.ndarray:
        """Get the data which the given item is currently displaying."""
        pass

    @abstractmethod
    def set_data(self, data: np.ndarray) -> None:
        """
        Replace the entire data of the item with the passed one.

        Args:
            item: Data Visualization item which should display the passed data
            data: N-Dimensional array of data the given item should display
        """
        pass

    @abstractmethod
    def add_data(self, data: np.ndarray) -> None:
        """
        Add the passed data to the already shown one.

        Args:
            item: Data Visualization item which should display the passed data
            data: N-Dimensional array of data the given item should display
        """
        pass


class PyQtGraphPlot(pg.PlotWidget, AbstractBasePlot):

    """PyQtGraph based implementation for the AbstractBasePlot."""

    library = PlottingLibraryEnum.PYQTGRAPH

    item_type_mapping: Dict[DataItemType, Tuple[Type, Dict]] = {
        DataItemType.CURVE: (pg.PlotDataItem, {"pen": "w", "symbol": None}),
        DataItemType.SCATTER: (pg.PlotDataItem, {"pen": None, "symbol": "o"}),
    }

    def __init__(self):
        AbstractBasePlot.__init__(self)
        pg.PlotWidget.__init__(self)

    def add_item(self, item_type) -> "PyQtGraphDataItem":
        item_class, params = self.item_type_mapping.get(item_type, (None, {}))
        if item_class is not None and isinstance(params, Dict):
            item = item_class(**params)
            self.addItem(item)
            return PyQtGraphDataItem(item)
        else:
            raise ValueError(f"For data item type {item_type} is no fitting "
                             f"item is defined.")

    def set_range(self, view_range):
        if self.plotItem.vb.autoRangeEnabled():
            self.plotItem.vb.disableAutoRange()
        self.plotItem.vb.setRange(xRange=view_range[0],
                                  yRange=view_range[1],
                                  padding=0.0,
                                  disableAutoRange=True)

    def get_range(self):
        return self.plotItem.vb.viewRange()


class PyQtGraphDataItem(AbstractDataItem):

    """PyQtGraph Wrapper for PlotDataItems etc."""

    def get_data(self):
        if isinstance(self._item, pg.PlotDataItem):
            return self._item.getData()

    def set_data(self, data):
        if isinstance(self._item, pg.PlotDataItem):
            if len(data) == 2:
                self._item.setData(x=data[0], y=data[1])

    def add_data(self, data):
        if isinstance(self._item, pg.PlotDataItem):
            if len(data) == 2:
                x, y = self._item.getData()
                x.append(data[0])
                y.append(data[1])
                x = x[len(data[0]):]
                y = y[len(data[1]):]
                self._item.setData(x=x, y=y)


class MatPlotLibPlot(AbstractBasePlot):

    library = PlottingLibraryEnum.MATPLOTLIB

    item_type_mapping: Dict[DataItemType, Tuple[Type, Dict]] = {
        DataItemType.CURVE: (Line2D, {
            "xdata": [],
            "ydata": [],
            "linestyle": "-",
        }),
        DataItemType.SCATTER: (Line2D, {
            "xdata": [],
            "ydata": [],
            "linestyle": "",
            "marker": "o",
        }),
    }

    def __init__(self):
        AbstractBasePlot.__init__(self)
        QtWidgets.QWidget.__init__(self)
        self._figure: Figure = Figure()
        self._canvas: FigureCanvas = FigureCanvas(self._figure)
        self._plot: Axes = self._figure.subplots()
        self._toolbar = NavigationToolbar(canvas=self._canvas,
                                          parent=self)
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self._toolbar)
        self._layout.addWidget(self._canvas)
        self.setLayout(self._layout)

    def add_item(self, item_type) -> "MatPlotLibDataItem":
        item_class, params = self.item_type_mapping.get(item_type, (None, {}))
        if item_class is not None and isinstance(params, Dict):
            item = item_class(**params)
            self._plot.add_artist(item)
            return MatPlotLibDataItem(self._canvas, item)
        else:
            raise ValueError(f"For data item type {item_type} is no fitting "
                             f"item is defined.")

    def set_range(self, view_range):
        self._plot.set_xlim(left=view_range[0][0], right=view_range[0][1])
        self._plot.set_ylim(bottom=view_range[1][0], top=view_range[1][1])
        self._canvas.draw()

    def get_range(self):
        x = self._plot.get_xlim()
        y = self._plot.get_ylim()
        return x, y


class MatPlotLibDataItem(AbstractDataItem):

    """Wrapper for Line2D objects etc."""

    def __init__(self, canvas: FigureCanvas, data_item: Any):
        super().__init__(data_item)
        self._canvas = canvas

    def get_data(self):
        if isinstance(self._item, Line2D):
            return self._item.get_data()

    def set_data(self, data):
        if isinstance(self._item, Line2D):
            self._item.set_data(data)
        self._canvas.draw()

    def add_data(self, data):
        if isinstance(self._item, Line2D):
            x, y = self._item.get_data()
            x.append(data[0])
            y.append(data[1])
            x = x[len(data[0]):]
            y = y[len(data[1]):]
            data = np.array([x, y])
            self._item.set_data(data)
