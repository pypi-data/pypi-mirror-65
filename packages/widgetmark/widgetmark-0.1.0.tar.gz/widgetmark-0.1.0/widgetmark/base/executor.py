import time
from typing import List, Optional, cast
from abc import ABC, abstractmethod
import logging
import traceback
import cProfile
import pstats
from .benchmark import (AbstractBenchmarkWindow,
                        UseCase,
                        UseCaseResult,
                        BenchmarkRuntimeContext,
                        GuiBackend)

logger = logging.getLogger(__name__)


class AbstractBenchmarkExecutor(ABC):

    gui_backend: Optional[GuiBackend] = None

    def __init__(self):
        ABC.__init__(self)
        self._runtime_context = BenchmarkRuntimeContext(executor=self)
        # Performance metrics
        self._last_time = 0.0
        self._execution_counter: int = 0
        self._timing_recorder: List[float] = []
        # self._output_stream = io.StringIO()
        self._profile_stats: Optional[pstats.Stats] = None
        self._current_profiler: Optional[cProfile.Profile] = None
        # Will be set later
        self._window: Optional[AbstractBenchmarkWindow] = None
        self._result: Optional[UseCaseResult] = None

    def set_window(self, window: AbstractBenchmarkWindow) -> None:
        self._window = window

    def launch(self, profile: bool = False) -> UseCaseResult:
        """Start the execution of the Benchmark"""
        if self._window is None:
            raise Exception("Before launching the Executor a benchmarking "
                            "window has to be set.")
        self._window.use_case.runtime_context = self._runtime_context
        self._last_time = time.time()
        try:
            self._window.integrate_use_case_widget()
        except Exception as e:
            # Catch exceptions raised when executing the Use Case
            logger.debug(traceback.format_exc())
            return UseCaseResult(
                use_case=self._window.use_case,
                exception=e,
            )
        self._window.prepare_window()
        self._launch()
        return cast(UseCaseResult, self._result)

    @property
    def current_run(self) -> int:
        return len(self._timing_recorder)

    @property
    def completed(self) -> bool:
        if self._window is not None:
            return self.current_run > self._window.use_case.repeat
        return False

    @property
    def timed_out(self) -> bool:
        if self._window is not None:
            timeout = self._window.use_case.timeout
            return timeout is not None and self.total_time > timeout
        return False

    @property
    def use_case(self) -> UseCase:
        if self._window is not None:
            return self._window.use_case
        else:
            raise ValueError("No window has yet been set, which is needed "
                             "to accessing the use case it is based on.")

    @property
    def total_time(self) -> float:
        return sum(self._timing_recorder)

    @property
    def avg_timing(self):
        if self._timing_recorder:
            return sum(self._timing_recorder) / len(self._timing_recorder)
        else:
            return 1.0

    @property
    def operations_per_second(self):
        return 1.0 / self.avg_timing

    @property
    def result(self) -> Optional[UseCaseResult]:
        if self._result is None:
            logger.debug("There are no results for the "
                         "benchmark yet available.")
        return self._result

    # ~~~~~~~~~~ PRIVATE ~~~~~~~~~~

    def _redraw_operation(self):
        """
        Execute one operation which triggers the widget redraw.
        This function should be used in the implementation of
        _launch().
        """
        try:
            self._profile()
            self._window.operate()
        except Exception as e:
            # Catch exceptions raised when executing the Use Case
            self._result = self._complete(exception=e)
            logger.debug(traceback.format_exc())
        self._record_current_time()
        self._check_if_completed()
        # self._window.process_events()

    def _profile(self) -> None:
        """
        Add the last recorded profile to the profiling stats and restart the
        profiler, if the use case has the profile flag set.
        """
        if self.use_case.profile:
            if self._profile_stats is None:
                self._profile_stats = pstats.Stats()
            if self._current_profiler is not None:
                self._current_profiler.disable()
                self._profile_stats.add(self._current_profiler)
            # TODO: use clear() instead of always creating a new profile
            self._current_profiler = cProfile.Profile()
            self._current_profiler.enable()

    def _check_if_completed(self):
        """
        Check if the Benchmark is completed. If the benchmark is completed,
        call the completion handler, which is implemented by the executor
        subclass.
        """
        if self.completed:
            self._result = self._complete()
        elif self.timed_out:
            logger.debug(f"Use case {type(self.use_case).__name__} "
                         f"timed out after taking more than "
                         f"{self.use_case.timeout} seconds.")
            self._result = self._complete(timed_out=True)
        self._execution_counter += 1

    def _record_current_time(self):
        """Save the current timestamp for later evaluation."""
        now = time.time()
        delta = now - self._last_time
        self._last_time = now
        self._timing_recorder.append(delta)

    # ~~~~~~~~~~ ABSTRACT ~~~~~~~~~~

    @abstractmethod
    def _launch(self):
        """Launch the benchmark"""
        pass

    @abstractmethod
    def _complete(self,
                  timed_out: bool = False,
                  exception: Optional[Exception] = None) -> UseCaseResult:
        """Handle the completion of the Benchmark"""
        pass
