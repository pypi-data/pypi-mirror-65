import time
from qtpy import QtWidgets
import widgetmark


class SuperSlowQLabel(QtWidgets.QLabel):

    """Simulation of a widget with a very slow Operation."""

    def setText(self, *args, **kwargs):
        """
        Before setting the text, we block the gui thread for 100msecs,
        which results in ~10 operations per second.
        """
        time.sleep(0.1)
        super().setText(*args, **kwargs)


class SetTextUseCase(widgetmark.UseCase):

    backend = widgetmark.GuiBackend.QT
    goal = 30.0
    minimum = 20.0
    tolerance = 0.05
    repeat = 50

    def setup_widget(self):
        self._widget = SuperSlowQLabel()
        return self._widget

    def operate(self):
        # Unexpected slow operation, which takes up to 100 ms -> setText(...)
        self._widget.setText(f"This label was changed "
                             f"{self.runtime_context.current_run} times.")
