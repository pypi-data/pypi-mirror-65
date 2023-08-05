"""
WIDGETMARK is a Performance Analysis Framework for GUI components
based on user defined use cases. Use Cases can be defined in classes
contained in separate files and are derived from widgetmark.UseCase.
These files will be searched recursively starting from the directory
widgetmark was started in. The default naming pattern is "bench_*.py".
"""

# TODO: print it somewhere
title = "\n".join([
    "",
    "          _     _            _                        _",
    "         (_)   | |          | |                      | |",
    "__      ___  __| | __ _  ___| |_ _ __ ___   __ _ _ __| | __",
    "\\ \\ /\\ / / |/ _` |/ _` |/ _ \\ __| '_ ` _ \\ / _` | '__| |/ /",
    " \\ V  V /| | (_| | (_| |  __/ |_| | | | | | (_| | |  |   <",
    "  \\_/\\_/ |_|\\__,_|\\__, |\\___|\\__|_| |_| |_|\\__,_|_|  |_|\\_\\",
    "                   __/ |",
    "                  |___/",
    "",
])

import signal
import logging
import argparse
from contextlib import contextmanager
import sys
from typing import Dict, Tuple, Union, List, cast
from snakeviz.cli import main as snakviz_main
from .loader import BenchmarkLoader, FileLocation
from .cli_view import PrintView, Color

logger = logging.getLogger(__name__)


class ArgumentNamespace(argparse.Namespace):

    """This class is only for auto completion purposes."""

    profile_output: str = "./profiles/"
    should_profile: bool = False
    pattern: str = ""
    locations: List[FileLocation] = []
    loglevel: str = ""
    visualize: bool = False


class CLI:

    _args: Dict[Tuple[str, ...], Dict[str, Union[str, bool, List[str]]]] = {
        ("-o", "--profile-output"): {
            "dest": "profile_output",
            "metavar": "PROFILE_FILES_LOCATION",
            "default": ArgumentNamespace.profile_output,
            "help": "Specify in which directory the profile files "
                    "should be saved in. The default is a directory "
                    "'profiles' in your current working directory. ",
        },
        ("-p", "--profile"): {
            "dest": "should_profile",
            "action": "store_true",
            "help": "If set, WidgetMark will create a profile using "
                    "the Python module cProfile to gain more insights "
                    "into performance of a widget. Activating profile "
                    "will introduce a small additional overhead which "
                    "will decrease performance. ",
        },
        ("locations",): {
            "nargs": "*",
            "help": "File or folder where the benchmark use cases are "
                    "located. It is additionally possible to specify "
                    "for passed files, which UseCases should be executed "
                    "by adding its name as 'folder/file.py::UseCaseName'. "
                    "UseCaseName can be a regular expression as well "
                    "'folder/file.py::.*Case.*'.",
        },
        ("--pattern",): {
            "dest": "pattern",
            "metavar": "USE_CASE_FILE_NAME_PATTERN",
            "help": "File Pattern for the Benchmark Files. Wildcards "
                    "are used in glob.glob(), e.g. 'bench_*.py'.",
        },
        ("--visualize", ): {
            "dest": "visualize",
            "action": "store_true",
            "help": "Start SNAKEVIZ with the profile output directory. "
                    "SNAKEVIZ allows you to conveniently explore the "
                    "recorded profiles in you web browser. To learn more "
                    "about its usage and features, visit "
                    "http://jiffyclub.github.io/snakeviz/",
        },
        ("--loglevel",): {
            "dest": "loglevel",
            "metavar": "LOGGING_MODULE_LEVEL",
            "choices": ["CRITICAL",
                        "ERROR",
                        "WARNING",
                        "INFO",
                        "DEBUG",
                        "NOTSET"],
            "help": "Set the Loggers Level to the passed one.",
        },
    }
    """Command Line Arguments."""

    def __init__(self):
        """
        Command Line Interface for the WidgetMark Framework, which allows
        using the BenchmarkLoader class from command line.
        """
        self._args: ArgumentNamespace = self._setup_command_line_args()
        self._loader = BenchmarkLoader(locations=self._args.locations,
                                       file_pattern=self._args.pattern,
                                       with_profiler=self._args.should_profile)

    def exec(self):
        """Load the Benchmark Files and Execute them"""
        PrintView.print_divider(message="WIDGET-MARK",
                                colors=Color.BOLD)
        with interrupt_signal_handled(_during_exec):
            self._loader.load()
            self._loader.run()
        PrintView.print_results(results=self._loader.results,
                                profile_output=self._args.profile_output)
        PrintView.print_divider(colors=Color.BOLD)
        if self._args.should_profile:
            if self._args.visualize:
                global profile_location
                profile_location = self._args.should_profile
                with interrupt_signal_handled(_during_snake_viz):
                    snakviz_main([self._args.should_profile])
            else:
                print(f"To view your profiles, run"
                      f" 'snakeviz {self._args.should_profile}'.")
                PrintView.print_divider(message="END OF SESSION",
                                        colors=Color.BOLD)

    def _setup_command_line_args(self) -> ArgumentNamespace:
        """Set up, parse and handle command line arguments."""
        parser = argparse.ArgumentParser(description=__doc__)
        for keys, values in self._args.items():
            parser.add_argument(*keys, **values)  # type: ignore
        args = parser.parse_args()
        # Log Level for the Application
        if args.loglevel:
            CLI._set_log_level(args.loglevel)
            del args.loglevel
        # File Locations
        if not args.locations:
            args.locations = BenchmarkLoader.DEFAULT_LOCATION
        for index, location in enumerate(args.locations):
            args.locations[index] = FileLocation(location=location)
        # Global Benchmark file Pattern
        if not args.pattern:
            args.pattern = BenchmarkLoader.DEFAULT_PATTERN
        return cast(ArgumentNamespace, args)

    @staticmethod
    def _set_log_level(log_level: str):
        """Set the logging packages log level to the passed level."""
        import logging
        level = getattr(logging, log_level)
        logging.basicConfig(level=level)


# ~~~~~~~~~~~~~~~~~~~~~~~~~ Interrupt Signal Handling ~~~~~~~~~~~~~~~~~~~~~~~~~


@contextmanager
def interrupt_signal_handled(new):
    """Context manager for handling keyboard interrupt signals."""
    old = signal.signal(signal.SIGINT, new)
    try:
        yield new
    finally:
        signal.signal(signal.SIGINT, old)


def _during_exec(_signal, _frame):
    print()
    PrintView.print_divider(message="SESSION INTERRUPTED",
                            colors=Color.BOLD)
    sys.exit(0)


profile_location = ""


def _during_snake_viz(_signal, _frame):
    print(f"\nTo reopen snakeviz, run 'snakeviz {profile_location}'.")
    PrintView.print_divider(message="END OF SESSION",
                            colors=Color.BOLD)
    sys.exit(0)
