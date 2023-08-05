import widgetmark
from widgetmark.cli.cli_view import _get_bar_color, Color


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Bar Graph printing ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class ColorTestsUseCase(widgetmark.UseCase):

    backend = widgetmark.GuiBackend.QT
    goal = 50.0
    minimum = 40.0
    tolerance = 0.1
    repeat = 1

    def setup_widget(self):
        return None

    def operate(self):
        pass


def test_color_yellow():
    result = widgetmark.UseCaseResult(
        use_case=ColorTestsUseCase(),
        operations_per_second=43.4,
    )
    assert _get_bar_color(result) == Color.YELLOW


def test_color_min_yellow():
    result = widgetmark.UseCaseResult(
        use_case=ColorTestsUseCase(),
        operations_per_second=36,
    )
    assert _get_bar_color(result) == Color.YELLOW


def test_color_green():
    result = widgetmark.UseCaseResult(
        use_case=ColorTestsUseCase(),
        operations_per_second=47.4,
    )
    assert _get_bar_color(result) == Color.GREEN


def test_color_min_green():
    result = widgetmark.UseCaseResult(
        use_case=ColorTestsUseCase(),
        operations_per_second=45,
    )
    assert _get_bar_color(result) == Color.GREEN


def test_color_bigger_than_goal():
    result = widgetmark.UseCaseResult(
        use_case=ColorTestsUseCase(),
        operations_per_second=64.4,
    )
    assert _get_bar_color(result) == Color.GREEN


def test_color_red():
    result = widgetmark.UseCaseResult(
        use_case=ColorTestsUseCase(),
        operations_per_second=21.2,
    )
    assert _get_bar_color(result) == Color.RED


def test_color_zero():
    result = widgetmark.UseCaseResult(
        use_case=ColorTestsUseCase(),
        operations_per_second=0.0,
    )
    assert _get_bar_color(result) == Color.RED


def test_negative():
    result = widgetmark.UseCaseResult(
        use_case=ColorTestsUseCase(),
        operations_per_second=-5.4,
    )
    assert _get_bar_color(result) == Color.RED
