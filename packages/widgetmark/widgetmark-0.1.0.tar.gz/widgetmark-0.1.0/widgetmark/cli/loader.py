from typing import List, Dict
import glob
import os
import logging
import traceback
from ..base.benchmark import UseCaseResult
from ..base.launcher import Launcher, InvalidBenchmarkError, BenchmarkFile

logger = logging.getLogger(__name__)


class FileLocation:

    def __init__(self, location: str):
        """Wrapper class for file locations + a class name filter."""
        loc = location.split("::")
        self.file_location: str = loc[0]
        self.class_name_filter: str = loc[1] if len(loc) > 1 else ""
        self._validate()

    def _validate(self):
        if os.path.isdir(self.file_location) and self.class_name_filter:
            logger.debug(f"Ignoring class name filter "
                         f"{self.class_name_filter}, since passed path "
                         f"is a directory.")
            self.class_name_filter = ""

    def __str__(self):
        if self.class_name_filter:
            return f"{self.file_location}::{self.class_name_filter}"
        return self.file_location


class BenchmarkLoader:

    DEFAULT_PATTERN: str = "bench_*.py"
    DEFAULT_LOCATION: List[str] = [os.getcwd()]

    def __init__(self,
                 locations: List[FileLocation],
                 file_pattern: str = DEFAULT_PATTERN,
                 with_profiler: bool = False):
        """
        The Benchmark Loader class is the central class for loading and
        executing benchmark files with the WidgetMark.

        Args:
            locations: A list of paths were to look for benchmarks
            file_pattern: File pattern for the benchmark files
            with_profiler: Profile the benchmark during execution
        """
        self._locations: List[FileLocation] = locations
        self._pattern: str = file_pattern
        self._profile: bool = with_profiler
        self._benchmark_files: List[BenchmarkFile] = []
        self._results: Dict[BenchmarkFile, List[UseCaseResult]] = {}

    def load(self) -> None:
        """
        Load the Benchmark Files from the specified locations with the
        specified file pattern.
        """
        for location in self._locations:
            path = location.file_location
            use_case_name = location.class_name_filter
            logger.debug(f"Collecting benchmarks matching the pattern "
                         f"'{self._pattern}' from {str(location)}.")
            files = []
            # Find files
            if os.path.isdir(path):
                files = glob.glob(f"{path}/**/{self._pattern}",
                                  recursive=True)
            elif os.path.isfile(path):
                files = glob.glob(path)
            # Wrap files and filters and save them
            for file in files:
                self._benchmark_files.append(BenchmarkFile(file,
                                                           use_case_name))
            logger.debug(f"{len(files)} Benchmark Files found in "
                         f"{location.file_location}.")
        logger.debug(f"{len(self._benchmark_files)} Benchmarks were "
                     f"loaded in total.")

    def run(self) -> None:
        """Run a list of use cases defined in a benchmark files."""
        if not self._benchmark_files:
            logger.error("Nothing to execute.")
        else:
            for file in self._benchmark_files:
                try:
                    file_results = Launcher(file).run(profile=self._profile)
                    self._results[file] = self._results.get(file, []) \
                        + file_results
                except InvalidBenchmarkError:
                    logger.error("Benchmark could not be executed due to an "
                                 "error in its definition.")
                except Exception as e:
                    logger.error(f"{type(e).__name__} during Execution.")
                    logger.debug(traceback.format_exc())

    @property
    def benchmark_files(self) -> List[str]:
        return [str(file) for file in self._benchmark_files]

    @property
    def results(self) -> Dict[BenchmarkFile, List[UseCaseResult]]:
        return self._results
