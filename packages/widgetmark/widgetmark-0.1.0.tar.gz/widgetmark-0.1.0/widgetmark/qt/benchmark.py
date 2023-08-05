from qtpy.QtWidgets import QMainWindow

from ..base.benchmark import AbstractBenchmarkWindow, UseCase, GuiBackend
from .util import make_qt_abc_meta


class QtWindow(AbstractBenchmarkWindow,
               QMainWindow,
               metaclass=make_qt_abc_meta(QMainWindow)):  # type: ignore

    """
    Abstract Base class for all benchmarks to define a common
    interface that can be used by the launcher to run it.

    This base class provides an empty QMainWindow, which will
    contain the widget, which's performance should be tested.
    To write a benchmark for your own widget, subclass this
    Benchmark Window and implement all abstract methods.
    """

    gui_backend = GuiBackend.QT

    def __init__(self, use_case: UseCase):
        QMainWindow.__init__(self)
        AbstractBenchmarkWindow.__init__(self, use_case=use_case)
        self.setWindowTitle(type(use_case).__name__)
        self.resize(800, 600)

    @property
    def max_repeat(self) -> int:
        return self._use_case.repeat

    def next_operation(self):
        """
        To make sure, that the widget does not skip on calling update() in
        some cases, we want to call update() by hand. To make sure that there
        are no duplicated redraws, we filter out all QPaintEvents that might be
        coming from the redraw_trigger.
        """
        # self._repaint_filter.block()
        self.redraw_trigger()
        # self._repaint_filter.unblock()
        # self.central_widget.update()
        # self._repaint_filter.block()

    def integrate_use_case_widget(self):
        widget = self._use_case.setup_widget()
        if widget is not None:
            self.setCentralWidget(widget)

    def widget(self):
        return self.centralWidget()

    def prepare_window(self):
        self.show()
