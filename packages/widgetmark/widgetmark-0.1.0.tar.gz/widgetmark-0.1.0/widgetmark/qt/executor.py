from typing import Optional, Type
from qtpy.QtCore import QTimer, QObject, QEvent
from qtpy.QtWidgets import QApplication
from ..base.executor import AbstractBenchmarkExecutor
from ..base.benchmark import UseCaseResult, GuiBackend
from .util import make_qt_abc_meta


class InteractionEventFilter(QObject):

    """
    To prevent unwanted interactions with the widget during
    use case execution, we will filter out all interaction.
    """

    filter = [QEvent.MouseButtonDblClick,
              QEvent.MouseButtonPress,
              QEvent.MouseButtonRelease,
              QEvent.MouseTrackingChange,
              QEvent.GrabMouse,
              QEvent.UngrabMouse,
              QEvent.Move,
              QEvent.DragEnter,
              QEvent.DragLeave,
              QEvent.DragMove]

    def eventFilter(self, o: QObject, e: QEvent):
        """Filter out all Mouse Clicks, single or double"""
        if e.type() in InteractionEventFilter.filter:
            e.ignore()
            return True
        return super().eventFilter(o, e)

    @classmethod
    def get_event_filter(cls: Type["InteractionEventFilter"],
                         app: QApplication):
        if not getattr(cls, "instance", None):
            cls.instance = InteractionEventFilter(parent=app)
        return cls.instance


class QtBenchmarkExecutor(QObject,
                          AbstractBenchmarkExecutor,
                          metaclass=make_qt_abc_meta(QObject)):  # type: ignore
    """
    The Benchmark Executor is responsible for executing the operations which
    trigger the widget's redraw, which is supposed to be benchmarked. We use
    the QTimer for executing a loop of this operation(s) to make sure that we
    do not create a blocking benchmark and  allow the QApplication to return
    to the EventLoop to process events.
    """

    gui_backend = GuiBackend.QT

    def __init__(self):
        QObject.__init__(self)
        AbstractBenchmarkExecutor.__init__(self)
        self._app = QtBenchmarkExecutor._prepare_qapp()

    def _launch(self):
        self._timer: QTimer = QTimer()
        self._timer.timeout.connect(self._redraw_operation)
        self._timer.start(0)
        self._app.exec()

    def _complete(self,
                  timed_out: bool = False,
                  exception: Optional[Exception] = None) -> UseCaseResult:
        self._timer.stop()
        self._app.closeAllWindows()
        self._app.quit()
        self._app.processEvents()
        return UseCaseResult(use_case=self.use_case,
                             operations_per_second=self.operations_per_second,
                             profiling_stats=self._profile_stats,
                             timed_out=timed_out,
                             exception=exception)

    @staticmethod
    def _prepare_qapp():
        """Prepare QApplication instance and install event filters."""
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
            app.installEventFilter(
                InteractionEventFilter.get_event_filter(app))
        return app
