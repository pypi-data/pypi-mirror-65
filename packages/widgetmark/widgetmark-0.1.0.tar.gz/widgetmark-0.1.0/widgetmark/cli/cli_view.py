"""
Utilities for the CLI we do not want to include into __main__.py
to not pollute it.
"""

from setuptools import find_packages
from pkgutil import iter_modules
import enum
import os
import logging
from typing import (
    Optional,
    List,
    Union,
    Tuple,
    TYPE_CHECKING,
    cast,
    Dict,
    Pattern,
)
import inspect
import pstats
import errno
import marshal
import re
if TYPE_CHECKING:
    from ..base import UseCaseResult

from .loader import BenchmarkFile

logger = logging.getLogger(__name__)

_unicode_triangle = "\u25B6"


class Color(enum.Enum):

    PURPLE = "\033[35m"
    CYAN = "\033[36m"
    BLUE = "\033[34m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


class PrintView:

    @staticmethod
    def print(
            *args,
            colors: Union[Color, List[Color], None] = None,
            indent: Union[int, str] = 0,
    ) -> None:
        """
        Convenient API for printing colored messages.

        Args:
            *args: Messages which should be printed
            colors: Colors from terminal the Color Enum
            indent: How many characters should the message be indented
        """
        if not colors:
            colors = []
        elif isinstance(colors, Color):
            colors = [colors]
        if isinstance(indent, int):
            indent = "".join([" " for _ in range(indent)])
        for message in args:
            print("".join([c.value for c in colors]) + indent
                  + message + Color.END.value)

    @staticmethod
    def print_divider(message: str = "",
                      width: Optional[int] = None,
                      soft_divider: bool = False,
                      **kwargs) -> None:
        # Set width
        window_width = _terminal_size(fallback=(80, 25))[0]
        if width is None or width > window_width:
            width = window_width
        # Trim message if necessary
        message = message.strip()
        if len(message) > width:
            message = message[:width - 4] + " ..."
        if message:
            message = " " + message + " "
        # Create Line to Print
        if soft_divider:
            divider = "\u2505"
        else:
            divider = "\u2501"
        div = "".join([divider for _ in range(
            int((width - len(message)) / 2))])
        line = div + message + div
        line += div[:width - len(line)]
        PrintView.print(line, **kwargs)

    @staticmethod
    def print_results(
            results: Dict[BenchmarkFile, List["UseCaseResult"]],
            profile_output: str = "",
    ) -> None:
        """Visualize the File results as a bar graph in the Terminal."""
        r: List["UseCaseResult"] = []
        for file, file_results in results.items():
            file_name = os.path.basename(file.file_location)
            PrintView.print(f"{_unicode_triangle} {file_name}",
                            colors=Color.BOLD)
            grouped_by_name: Dict[str, List["UseCaseResult"]] = {}
            for result in file_results:
                current = grouped_by_name.get(result.use_case_name, [])
                current.append(result)
                grouped_by_name[result.use_case_name] = current
            for uc, rs in grouped_by_name.items():
                PrintView._print_results_of_use_case(
                    use_case=uc,
                    results=rs,
                    profile_output=profile_output,
                )
            r += file_results
        PrintView.print_summary(results=r)

    @staticmethod
    def _print_results_of_use_case(use_case: str,
                                   results: List["UseCaseResult"],
                                   profile_output: str):
        prefix = "\u2514 "
        if len(results) > 1:
            PrintView.print(prefix + use_case, indent=2)
        for v in results:
            if len(results) == 1:
                name = v.use_case_name
                indent = 2
            else:
                name = v.use_case_params
                indent = 4
            if v.failed:
                PrintView._print_exception(name=name,
                                           line_prefix=prefix,
                                           indent=indent,
                                           exception=v.exception)
            else:
                PrintView._print_bar(name=name,
                                     line_prefix=prefix,
                                     indent=indent,
                                     color=_get_bar_color(result=v),
                                     value=v.operations_per_second,
                                     goal=v.goal_operations_per_second,
                                     minimum=v.minimum_operations_per_second,
                                     name_len=_terminal_size((80, 25))[0] - 40)
                if v.timed_out:
                    PrintView._print_time_out(line_prefix=prefix,
                                              indent=indent + len(prefix),
                                              timeout=v.timeout)
                if v.profile_stats is not None:
                    PrintView._persist_profile(stats=v.profile_stats,
                                               use_case=v.use_case_name,
                                               params=v.use_case_params,
                                               line_prefix=prefix,
                                               indent=indent + len(prefix),
                                               profile_output=profile_output)

    @staticmethod
    def print_summary(results: List["UseCaseResult"]) -> None:
        """
        Print a line containing a summary of all executed use cases and their
        results. It will list how many of them were green, yellow and red, how
        many failed and how many timed out.
        """
        green = [result for result in results
                 if _get_bar_color(result) == Color.GREEN]
        yellow = [result for result in results
                  if _get_bar_color(result) == Color.YELLOW]
        red = [result for result in results
               if _get_bar_color(result) == Color.RED]
        failed = [result for result in results if result.failed]
        timed_out = [result for result in results if result.timed_out]
        bo = Color.BOLD.value
        gr = Color.GREEN.value
        ye = Color.YELLOW.value
        re = Color.RED.value
        en = Color.END.value
        PrintView.print_divider()
        PrintView.print(f"Summary (Executed {len(results)} Use Cases)",
                        colors=Color.BOLD)
        PrintView.print(f"{bo}{gr}GOAL{en}        {len(green)} Use Cases")
        PrintView.print(f"{bo}{ye}MIN{en}         {len(yellow)} Use Cases")
        PrintView.print(f"{bo}{re}NONE{en}        {len(red)} Use Cases")
        PrintView.print_divider(soft_divider=True)
        PrintView.print(f"{bo}{re}Exceptions{en}  {len(failed)} Use Cases")
        PrintView.print(f"{bo}{re}Timed Out{en}   {len(timed_out)} Use Cases")

    @staticmethod
    def _persist_profile(stats: pstats.Stats,
                         use_case: str,
                         params: str,
                         line_prefix: str,
                         indent: int,
                         profile_output: str):
        """
        Print the profiling stats and filter out
        """
        file = (f"{use_case}_{params}" if params else use_case) + ".profile"
        file = os.path.abspath(os.path.join(profile_output, file))
        _prepare_directory(file)
        PrintView.print(f"{line_prefix}Profile saved to {file}", indent=indent)
        # We want to filter out System calls as well as functions that are part
        # of the Framework
        stats = _get_cleaned(stats,
                             filtered_packages=widget_mark_install_path(),
                             filter_system_calls=True)
        # Write to file, can be viewed in snakeviz
        with open(file, "wb") as f:
            marshal.dump(stats, f)

    @staticmethod
    def _print_exception(name: str,
                         line_prefix: str,
                         indent: int,
                         exception: Optional[Exception],
                         name_len: int = 45) -> None:
        reason = type(exception).__name__ if exception else "Exception"
        name_cut = name[:name_len - 5] + " ... " \
            if len(name) > name_len else name
        label = ("{:<" + str(name_len) + "}").format(name_cut).format(name)
        message = f"{line_prefix}{label}: Failed due to {reason}."
        PrintView.print(message, colors=[Color.RED, Color.BOLD], indent=indent)

    @staticmethod
    def _print_time_out(timeout: float,
                        indent: int,
                        line_prefix: str = "") -> None:
        message = f"{line_prefix}Timed out after {timeout} seconds."
        PrintView.print(message, colors=[Color.RED, Color.BOLD], indent=indent)

    @staticmethod
    def _print_bar(name: str,
                   line_prefix: str,
                   indent: int,
                   color: Color,
                   goal: float,
                   minimum: float,
                   value: float,
                   name_len: int = 40):
        label = _prepare_bar_labels(name=name,
                                    line_prefix=line_prefix,
                                    indent=indent,
                                    goal=goal,
                                    minimum=minimum,
                                    name_len=name_len)
        bar = _prepare_bars(width=30,
                            goal=goal,
                            value=value,
                            color=color)
        truncated_value = "{:5.1f}".format(value)
        print(f"{label}: {bar} {truncated_value}")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Private ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def _terminal_size(fallback: Tuple[int, int]) -> Tuple[int, int]:
    """
    Try to get the size of the terminal window.
    If it fails, the passed fallback will be returned.
    """
    for i in (0, 1):
        try:
            window_width = os.get_terminal_size(i)
            return cast(Tuple[int, int], tuple(window_width))
        except OSError:
            continue
    return fallback


def get_class_that_defined_method(meth):
    try:
        for cls in inspect.getmro(meth.im_class):
            if meth.__name__ in cls.__dict__:
                return cls
    except Exception:
        pass
    return None


def _prepare_bar_labels(name: str,
                        line_prefix: str,
                        indent: int,
                        goal: float,
                        minimum: float,
                        name_len: int) -> str:
    gr = Color.GREEN.value
    ye = Color.YELLOW.value
    en = Color.END.value
    reference = f"GOAL={goal}, MIN={minimum}"
    line_prefix = "".join([" " for _ in range(indent)]) + line_prefix
    name_cut = name[:name_len - 3 - len(reference) - len(line_prefix)] + \
        "..." if len(name + reference) > name_len else name
    spaces = "".join("." for _ in range(
        name_len - len(name_cut + reference + line_prefix)))
    label = line_prefix + name_cut + ", " + spaces + reference
    label = label.replace("GOAL", f"{gr}GOAL{en}")
    label = label.replace("MIN", f"{ye}MIN{en}")
    return label


def _prepare_bars(goal: float,
                  value: float,
                  color: Color,
                  width: int) -> str:
    length = round(width * (value / goal))
    if length > width:
        length = width
    elif length < 1:
        length = 1
    blocks = "".join(["\u2588" for _ in range(length)])
    space = "".join([" " for _ in range(width - length)])
    return f"{color.value}{blocks}{Color.END.value}{space}"


def _prepare_directory(file: str):
    """Prepare the directory where the profile files will be saved in."""
    if not os.path.exists(os.path.dirname(file)):
        try:
            os.makedirs(os.path.dirname(file))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def _get_bar_color(result: "UseCaseResult") -> Color:
    if result.failed:
        return Color.END
    ops_ps = result.operations_per_second
    goal = result.goal_operations_per_second
    minimum = result.minimum_operations_per_second
    tolerance = result.operations_per_second_tolerance
    if ops_ps + minimum * tolerance < minimum:
        return Color.RED
    elif ops_ps + goal * tolerance < goal:
        return Color.YELLOW
    else:
        return Color.GREEN


def _get_cleaned(stats,
                 filtered_packages: Optional[List] = None,
                 filter_system_calls: bool = False):
    """
    To make the profiler stats easier to read, we want to filter out:
    1. Code from Site Packages
    2. Code belonging to the widgetmark Framework

    Template for the filter was the project:
    https://github.com/w0rp/filter-profiler-results

    Args:
        stats:

    Returns:
        Cleaned version of the passed stats
    """
    name_filter: List[Union[str, Pattern]] = []
    if filtered_packages is None:
        filtered_packages = []
    for package in filtered_packages:
        name_filter += _find_modules(package)
    if filter_system_calls:
        name_filter.append(re.compile(r"~|<string>|<frozen .*>"))
    filtered_stats = {
        key: (nc, cc, tt, ct, {
            caller_key: timing_tuple
            for caller_key, timing_tuple in
            callers.items()
            if should_include_stats(caller_key, name_filter)
        })
        for key, (nc, cc, tt, ct, callers) in stats.stats.items()
        if should_include_stats(key, name_filter)
    }
    return filtered_stats


def should_include_stats(stats_key, filename_filters):
    filename, line_number, symbol = stats_key
    for f in filename_filters:
        if isinstance(f, str) and f in filename:
            return False
        elif hasattr(f, "match") and re.match(f, filename):
            return False
    return True


def widget_mark_install_path() -> List[str]:
    """Get the path where the package widget-mark was installed to."""
    import widgetmark
    return widgetmark.__path__  # type: ignore  # mypy issue #1422


def _find_modules(path: str):
    """Find all modules of a package."""
    modules = set()
    for pkg in find_packages(path):
        for info in iter_modules([os.path.join(path, pkg.replace(".", "/"))]):
            if not info.ispkg:
                modules.add(os.path.join(pkg, info.name))
    return modules
