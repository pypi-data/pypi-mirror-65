import logging
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Optional, Dict, Union, List, TYPE_CHECKING
import pstats
if TYPE_CHECKING:
    from ..base.executor import AbstractBenchmarkExecutor

import numpy as np

logger = logging.getLogger(__name__)


class UseCase(ABC):

    """Abstract Base Class for Benchmarking Use Cases.

    All functions listed in this Base Class are mandatory to implement.
    For properties it is enough to define them as class attributes:

    Examples:

    >>> class MyUseCase(UseCase):
    >>>
    >>>    backend = GuiBackend.QT
    >>>    goal = 60.0
    >>>    # ...
    """

    parameters: Dict[str, List] = {}
    """Optional Parameterization for Use Cases."""

    timeout: Optional[float] = None
    """Optional Timeout in Seconds"""

    profile: bool = False
    """
    If set, the Use Case will be profiled no matter what command
    line options are passed.
    """

    def __init__(self):
        super().__init__()
        self.__runtime_context: Optional[BenchmarkRuntimeContext] = None
        self.__params: str = ""

    @property
    @abstractmethod
    def backend(self) -> "GuiBackend":
        """
        GUI backend which should be used for execution. Make sure that the
        backend is fitting to your widget.
        """
        pass

    @property
    @abstractmethod
    def goal(self) -> float:
        """
        Operations Per Second which are the expected goal.
        Use Cases achieving this goal will be marked in a
        green color.
        """
        pass

    @property
    @abstractmethod
    def minimum(self) -> float:
        """
        Operations Per Second which are expected at minimum.
        Use Cases achieving this minimum, but not the goal
        will be marked with a yellow color.
        """
        pass

    @property
    @abstractmethod
    def repeat(self) -> int:
        """
        How often should the operation defined in operate()
        be repeated? More repetition will lead to more
        precise results but longer duration.
        """
        pass

    @property
    @abstractmethod
    def tolerance(self) -> float:
        """
        Tolerance is a factor that is used when evaluating if the actual
        measured results meet the goal or minimum expectations.

        Tolerance = 0.1
        - 46.03 FPS meets the 50.0 FPS goal -> Green Bar

        Tolerance = 0.05
        - 46.03 FPS does not meet the 50.0 FPS goal, but the 30 FPS minimum
        -> Yellow Bar

        Returns:
            Tolerance Factor (normally between 0.0 and 1.0 for 0% to 100%
            Tolerance)
        """
        pass

    @abstractmethod
    def setup_widget(self) -> Any:
        """
        Instantiate the widget which should be benchmarked and return it.
        It is recommended to keep references to everything created, which
        you will later use in the operate() function (Widget, widget content,
        etc...).
        """
        pass

    @abstractmethod
    def operate(self):
        """
        Define the operation which's performance should be analysed.
        You should make sure that this operation is actually changing
        the widget as it is intended to, otherwise the Benchmark Results
        will be not representative.
        """
        pass

    @property
    def runtime_context(self) -> Optional["BenchmarkRuntimeContext"]:
        if self.__runtime_context is None:
            logger.debug("The Benchmark is not yet running, so there"
                         "is not runtime context yet.")
        return self.__runtime_context

    @runtime_context.setter
    def runtime_context(self, context: "BenchmarkRuntimeContext"):
        if context is not None:
            self.__runtime_context = context

    @property
    def params(self) -> str:
        return self.__params

    @params.setter
    def params(self, params: str) -> None:
        self.__params = params


class GuiBackend(Enum):

    """Enum representing different GUI backends."""

    QT = 0
    """Qt (PyQt) as the backend for all GUI operations."""


class BenchmarkRuntimeContext:

    def __init__(self, executor: "AbstractBenchmarkExecutor"):
        self.__executor: "AbstractBenchmarkExecutor" = executor

    @property
    def current_run(self) -> int:
        return self.__executor.current_run

    @property
    def avg_timing(self) -> float:
        return self.__executor.avg_timing

    @property
    def operations_per_second(self) -> float:
        return self.__executor.operations_per_second


class UseCaseResult:

    def __init__(self,
                 use_case: Union["UseCase", str],
                 operations_per_second: Optional[float] = None,
                 profiling_stats: Optional[pstats.Stats] = None,
                 timed_out: bool = False,
                 exception: Union[Exception, None] = None):
        """
        Benchmark results need to be derived from QObject to be usable
        as a data type in signals.

        Args:
            use_case: Use case which these results belong to
            operations_per_second: How many operations per second were
                                   achieved?
            timed_out: Was the Use Case quit before finish because it took
                       too long?
            exception: Optional exception that occurred on executing the
                       Use Case.
        """
        self._use_case = use_case
        self._ops_ps = operations_per_second
        self._timed_out = timed_out
        self._exception = exception
        self._profiling_stats = profiling_stats

    @property
    def failed(self) -> bool:
        """Check if the Execution of the Use Case has failed"""
        return self._exception is not None

    @property
    def timed_out(self) -> bool:
        """Check fi the Execution of the Use Case stopped due to a time out"""
        return self._timed_out

    @property
    def timeout(self) -> float:
        """
        Maximum time the use case is allowed to take. If the Use Case
        took longer to execute, it was stopped and marked as timed out.
        (See timed_out() to check if the use case timed out)
        """
        if isinstance(self._use_case, UseCase):
            if self._use_case.timeout is not None:
                return self._use_case.timeout
        return np.inf

    @property
    def profile_stats(self) -> Optional[pstats.Stats]:
        return self._profiling_stats

    @property
    def exception(self) -> Union[Exception, None]:
        """Get the exception raised by the Use Case, if one was raised."""
        return self._exception

    @property
    def use_case_name(self):
        """Name of the Use Case, which this results is based on."""
        if isinstance(self._use_case, str):
            return self._use_case
        return type(self._use_case).__name__

    @property
    def use_case_params(self):
        """Parameters of the use case"""
        if isinstance(self._use_case, str):
            return "No params"
        return self._use_case.params

    @property
    def operations_per_second(self):
        """How many operations per second were achieved."""
        return self._ops_ps

    @property
    def goal_operations_per_second(self) -> float:
        """The expectation for operations per second from the use case."""
        if isinstance(self._use_case, str):
            return 0.0
        return self._use_case.goal

    @property
    def minimum_operations_per_second(self) -> float:
        """The expectation for operations per second from the use case."""
        if isinstance(self._use_case, str):
            return 0.0
        return self._use_case.minimum

    @property
    def operations_per_second_tolerance(self) -> float:
        """The tolerance for operation per seconds comparisons"""
        if isinstance(self._use_case, str):
            return 0.0
        return self._use_case.tolerance


class AbstractBenchmarkWindow(ABC):
    """
    Abstract Base class for all benchmarks to define a common
    interface that can be used by the launcher to run it.

    This base class provides an empty QMainWindow, which will
    contain the widget, which's performance should be tested.
    To write a benchmark for your own widget, subclass this
    Benchmark Window and implement all abstract methods.
    """

    gui_backend: Optional[GuiBackend] = None

    def __init__(self, use_case: UseCase):
        ABC.__init__(self)
        # self._widget = use_case.setup_widget()
        self._use_case = use_case

    @property
    def use_case(self) -> UseCase:
        """Use Case the window is based on."""
        return self._use_case

    def operate(self):
        self._use_case.operate()

    @abstractmethod
    def integrate_use_case_widget(self):
        """Add the widget from the passed use case to the window."""
        pass

    @abstractmethod
    def widget(self):
        """Return the widget which was integrated into the window."""
        pass

    @abstractmethod
    def prepare_window(self):
        """
        Prepare the window for the Launch of the Benchmark.
        Implementations should include everything needed so the
        window appears on the screen (including any show() operation).
        """
        pass
