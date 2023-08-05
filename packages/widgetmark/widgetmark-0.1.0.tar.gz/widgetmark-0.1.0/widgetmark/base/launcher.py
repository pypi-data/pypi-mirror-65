"""
Launcher for starting a QApplication with a window which is
loaded from a python module that is passed as the parameter
"file" when invoking this script. The loaded window should
be a QMainWindow which inherits from the Benchmark class to
have a common interface for executing the Benchmark and
getting its results.
"""

import os
import re
import importlib.util
import itertools
import inspect
import logging
import traceback
from enum import Enum
from typing import Union, Type, List, Dict, Any, cast, Set
from dataclasses import dataclass

from .benchmark import (UseCaseResult,
                        UseCase,
                        GuiBackend,
                        AbstractBenchmarkWindow)
from .executor import AbstractBenchmarkExecutor

logger = logging.getLogger(__name__)


@dataclass(unsafe_hash=True)
class BenchmarkFile:

    """
    A Benchmark File is defined by a file location
    and an optional use_case_name which should be executed
    from that file.
    """

    file_location: str
    use_case_name: str = ""

    def __str__(self):
        if self.use_case_name:
            return f"{self.file_location}::{self.use_case_name}"
        return self.file_location


class InvalidBenchmarkError(Exception):
    pass


class InvalidUseCaseDefinitionError(Exception):
    pass


class Launcher:

    def __init__(
            self,
            use_case_classes: Union[str, BenchmarkFile, Type, List[Type]],
    ):
        """
        Class for launching any benchmark windows. This launcher can
        either be constructed from a passed class or from a class loaded
        from a given module path.

        Args:
            use_case_classes: A module location from file location,
                              BenchmarkFile dataclass or use case classes
        """
        self._use_case_classes: List[Type[UseCase]] = []
        if isinstance(use_case_classes, str):
            self._use_case_classes = self._import(
                file_name=use_case_classes,
                class_type=UseCase)
        elif isinstance(use_case_classes, BenchmarkFile):
            self._use_case_classes = self._import(
                file_name=use_case_classes.file_location,
                class_type=UseCase,
                name_filter=use_case_classes.use_case_name)
        elif (isinstance(use_case_classes, type)
              and issubclass(use_case_classes, UseCase)):
            self._use_case_classes = [use_case_classes]
        elif isinstance(use_case_classes, list):
            self._use_case_classes = use_case_classes
        else:
            raise TypeError(
                "The passed use cases do not have the right type")

    def run(self, profile: bool = False) -> List[UseCaseResult]:
        """Run all loaded use cases."""
        results: List[UseCaseResult] = []
        for use_case_class in self._use_case_classes:
            combs = self.get_params_combination(use_case_class.parameters)
            for comb in combs:
                try:
                    use_case: UseCase = use_case_class()
                    if profile:
                        use_case.profile = True
                    params_list = []
                    for name, value in comb.items():
                        setattr(use_case, name, value)
                        params_list.append(Launcher._readable_string(value))
                    use_case.params = ", ".join(params_list)
                except TypeError:
                    results.append(
                        UseCaseResult(
                            use_case=use_case_class.__name__,
                            exception=InvalidUseCaseDefinitionError(),
                        ),
                    )
                    logger.debug(traceback.format_exc())
                    continue
                executor = BackendResolver.executor_type(use_case.backend)()
                window = BackendResolver.window_type(
                    use_case.backend)(use_case=use_case)
                executor.set_window(window=window)
                results.append(executor.launch(profile=profile))
        return results

    # ~~~~~~~~~~~~~~~~~~~~ PRIVATE ~~~~~~~~~~~~~~~~~~~~

    @staticmethod
    def _import(file_name: str,
                class_type: Type,
                name_filter: str = "") -> List[Type[UseCase]]:
        """
        Try to import a benchmark window class from the module the given
        file path is referencing. First, see if any class is referenced
        by the BENCHMARK_CLASS or an other passed attribute and if not
        search for classes derived from
        """
        module_name: str = os.path.basename(file_name)
        logger.debug(f"Search for benchmark in module {module_name}.")
        path: str = file_name
        spec = importlib.util.spec_from_file_location(module_name, path)
        benchmark_module = importlib.util.module_from_spec(spec)
        if (spec.loader is not None
                and isinstance(spec.loader, importlib.abc.Loader)):
            spec.loader.exec_module(benchmark_module)
        else:
            raise InvalidBenchmarkError("Module {module_name} could not"
                                        "be loaded.")
        use_case_classes = Launcher._get_types_from_module(benchmark_module,
                                                           class_type)
        if name_filter:
            logger.debug(f"Filter the found {len(use_case_classes)} "
                         f"use case classes for name {name_filter}")
            use_case_classes = [cls for cls in use_case_classes
                                if re.match(name_filter, cls.__name__)]
        if not use_case_classes:
            raise InvalidBenchmarkError(f"No Use Case class could be "
                                        f"found in module {module_name}.")
        return cast(List[Type[UseCase]], use_case_classes)

    @staticmethod
    def _get_types_from_module(benchmark_module,
                               class_type: Type) -> List[Type]:
        loaded_cls: List[Type] = []
        for name, obj in inspect.getmembers(benchmark_module,
                                            inspect.isclass):
            if issubclass(obj, class_type):
                logger.debug(f"Found benchmark class {name} derived "
                             f"from {class_type.__name__}.")
                loaded_cls.append(obj)
        return loaded_cls

    @staticmethod
    def get_params_combination(
            params: Dict[str, List],
    ) -> List[Dict[str, Any]]:
        """
        Create a list of all possible parameters as a dictionary.

        Args:
            params: Dictionary of parameters mapped to all possible values

        Returns:
            List containing all different combinations of parameters

        Examples:
            Params: {'a': [0, 1], 'b': [2]}

            Returns: [{'a': 0, 'b': 2},{'a': 1, 'b': 2},]

            Params: {'a': [0]}

            Returns: [{'a': 0}]

            Params: {}

            Returns: [{}]
        """
        all_names = sorted(params)
        comb = itertools.product(*(params[name] for name in all_names))
        as_list = []
        for entry in comb:
            e = {}
            for i, n in enumerate(all_names):
                e[n] = entry[i]
            as_list.append(e)
        return as_list

    @staticmethod
    def _readable_string(value: Any) -> str:
        if isinstance(value, Enum):
            return value.name
        elif inspect.isclass(value):
            return value.__name__
        return str(value)


class BackendResolver:

    @staticmethod
    def window_type(gui_backend: GuiBackend) -> Type[AbstractBenchmarkWindow]:
        """Window Type for the given backend."""
        return cast(Type[AbstractBenchmarkWindow],
                    BackendResolver._get_gui_backend_subclass(
                        gui_backend,
                        AbstractBenchmarkWindow))

    @staticmethod
    def executor_type(
            gui_backend: GuiBackend,
    ) -> Type[AbstractBenchmarkExecutor]:
        """Executor Type for the given backend."""
        return cast(Type[AbstractBenchmarkExecutor],
                    BackendResolver._get_gui_backend_subclass(
                        gui_backend,
                        AbstractBenchmarkExecutor))

    @staticmethod
    def _get_gui_backend_subclass(gui_backend: GuiBackend, super_type: Type):
        """
        Get a subclass for the given type, which has the attribute gui_backend
        which is set to the passed one.
        """
        for cls in BackendResolver._all_subclasses(super_type):
            try:
                if cls.gui_backend == gui_backend:
                    return cls
            except AttributeError:
                pass
        raise ValueError(f"No subclass for {super_type} found "
                         f"for {gui_backend.name}.")

    @staticmethod
    def _all_subclasses(super_type: Type) -> Set[Type]:
        return set(super_type.__subclasses__()).union([
            s for c in super_type.__subclasses__()
            for s in BackendResolver._all_subclasses(c)
        ])
