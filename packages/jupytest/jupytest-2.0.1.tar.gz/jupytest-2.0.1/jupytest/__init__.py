"""
Unit and integration testing in a notebook

*** Building and running suites of tests ***

class Suite
    Method test (context manager)
Function fail

*** Reporting test results ***

Function report_results
Function summarize_results
Function detail_issues
Class Report (used as a subscriber plug-in to class Suite)

*** Delving deeper into test results (going beyond the tools described above) ***

Class Suite
    Property results
Class Result
    Sub-class Success
    Sub-class Error
        Sub-class Failure
    Method is_success
    Method is_failure
Class Frame

*** Customizing result reporting ***

Class Colorizer
    Function plain
    Function color
Class Emphasis
    Sub-class Plain
    Sub-class Color
Type TestNameFormatter
    Function ladder
    Function name_all
    Function quoter
Function detail_results
Function print_frame

*** Checking out the intricacies of test isolation ***

Function protect_environment

Happy jupytesting!
"""

from abc import ABC, abstractmethod
from copy import copy, deepcopy
from inspect import getframeinfo, Traceback, unwrap
from io import TextIOBase
import itertools
from linecache import getline
import sys
from traceback import walk_tb
from typing import Dict, List, Tuple, Iterator, Union, Iterable, Optional, Any, Callable, Mapping, Sequence

import colors
from IPython import get_ipython
from IPython.core.magic import register_cell_magic
from pygments import highlight
from pygments.lexers import Python3Lexer
from pygments.formatters import TerminalFormatter

class Result(ABC):
    """
    Result of a test. Indicates whether the test passed (was a success), and if it did not,
    whether it was a failure (as opposed to any other kind of issue).
    """

    @abstractmethod
    def is_success(self) -> bool:
        """True when an associated test run has passed."""
        raise NotImplementedError()

    def is_failure(self) -> bool:
        """True when an associated has not passed because a designed failure condition was met."""
        return False

    def as_dict(self) -> Dict:
        """Expresses this result as a dictionary suitable to structured data serialization."""
        return {"type": type(self).__name__}

class TestFailed(Exception):
    """
    Exception raised by this framework in order to mark a test run as a Failure.
    """

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason

def fail(reason: str = ""):
    "Marks some ongoing test as failed, with an optional reason for failure."
    raise TestFailed(reason)

class Success(Result):
    """
    Result for a test that passed.
    """
    def is_success(self) -> bool:
        return True

class Frame:
    """
    Information regarding a frame of a traceback. Provides more than the very limited
    code context that comes from standard library introspection tools.
    """

    def __init__(self, tb: Traceback, num_line: int, tags: Optional[List[str]] = None) -> None:
        self.num_line = num_line
        self.name_file = tb.filename
        self.function = tb.function
        self.tags = tags or []

    def context(self, before: int = 3, after: int = 3) -> List[Tuple[int, str]]:
        ctx = [(self.num_line, getline(self.name_file, self.num_line).rstrip())]
        for delta in range(1, before + 1):
            ctx.insert(0, (self.num_line - delta, getline(self.name_file, self.num_line - delta).rstrip()))
        for delta in range(1, after + 1):
            ctx.append((self.num_line + delta, getline(self.name_file, self.num_line + delta).rstrip()))

        # Clean up context: remove line-ending blanks and blank lines top and bottom
        # of the context blob.
        while len(ctx) > 0:
            for i in [0, -1]:
                if len(ctx[i][1]) == 0:
                    del ctx[i]
                    break
            else:
                break

        return ctx

    def as_dict(self, context_before: int = 3, context_after: int = 3) -> Dict:
        return {
            "file": self.name_file,
            "line": self.num_line,
            "function": self.function,
            "context": [[i, line] for i, line in self.context(context_before, context_after)],
            "tags": self.tags
        }

    def __str__(self) -> str:
        return f"File {self.name_file}, Line {self.num_line}, Function {self.function}"

    def __repr__(self) -> str:
        return str(self)

class Error(Result):
    """
    Non-passing test result due to an exception being raised.

    It is passed a set of common functions: the presence of these functions in the
    traceback of the exception are expected and normal, making their eventual
    reporting redundant and sort of trivial. The frames corresponding to these functions
    in the traceback summary kept by this object will be tagged as such.
    """
    TAG_COMMON = "common"

    def __init__(self, fns_common: Iterable[Callable]) -> None:
        super().__init__()
        self._type_exc: type
        self._value_exc: Any
        self._type_exc, self._value_exc, tb = sys.exc_info()
        if tb is None:
            raise RuntimeError("Can only instantiate this class when an exception has been raised.")

        codes_common = {unwrap(fn).__code__ for fn in fns_common}
        self._traceback: List[Frame] = []
        for frame_raw, num_line in walk_tb(tb):
            tags = []
            if frame_raw.f_code in codes_common:
                tags.append(Error.TAG_COMMON)
            self._traceback.append(Frame(getframeinfo(frame_raw), num_line, tags))

    def is_success(self) -> bool:
        return False

    @property
    def type_exc(self) -> type:
        """Returns the type of the exception associated to this result."""
        return self._type_exc

    @property
    def value_exc(self) -> Any:
        """Returns the exception raised in association to this test result."""
        return self._value_exc

    @property
    def traceback(self) -> List[Frame]:
        """
        Returns a summary of the stack trace associated to the exception that brought this test result.
        """
        return self._traceback

    def as_dict(self, context_before: int = 3, context_after: int = 3) -> Dict:
        d = super().as_dict()
        d.update(
            {
                "type_exc": self.type_exc.__name__,
                "value_exc": str(self.value_exc),
                "traceback": [frame.as_dict(context_before, context_after) for frame in self.traceback]
            }
        )
        return d

class Failure(Error):
    """
    Test result stemming from a condition check that failed, or a test run marked
    as a failure.
    """
    def __init__(self, reason: str, fns_common: Iterable[Callable]):
        super().__init__(fns_common)
        self._reason = reason

    @property
    def reason(self) -> str:
        "Reason given by the programmer as to why the test failed."
        return self._reason

    def is_failure(self) -> bool:
        return True

    def as_dict(self, context_before: int = 3, context_after: int = 3) -> Dict:
        d = super().as_dict(context_before, context_after)
        d["reason"] = self.reason
        return d

class Subscriber(ABC):
    """
    Object reacting to test results as they are generated by running tests.
    """

    @abstractmethod
    def on_result(self, name_test: str, result: Result) -> None:
        raise NotImplementedError()

TestFunction = Callable[..., None]


class Suite:
    """
    Suite of tests, gathering the result of multiple named test runs. Test code fragments
    are named using the `test()` decorator, or leveraging it indirectly by registering
    a shortcut cell magic.

    Test suites gets added functionality through a publish/subscribe system. Subscriber are
    special objects tied to the suite instance through its `|' (bit OR) operator. At the
    moment, the only event broadcast to all subscribers is the generation of a new test
    result (and its appending to the suite's log). For instance, the `Report` plug-in
    supports the suite by giving immediate feedback on a test's results. Thus, to
    instantiate a suite with this added feature, one would use code like

    suite = Suite() | Report()
    """

    def __init__(self, name_magic: str = "test") -> None:
        self._tests: Dict[str, List[Result]] = {}
        self._fns_common = [fail, self.test, self._run_cell_test]
        self._subscribers: List[Subscriber] = []

        ipython = get_ipython()
        if ipython and name_magic:
            register_cell_magic(name_magic)(lambda line, cell: self._test_cell(line, cell))

    def test(
        self,
        fn: Optional[TestFunction] = None,
        name: str = "",
        args: Sequence[Any] = [],
        kwargs: Mapping[str, Any] = {}
    ) -> Union[Callable[[TestFunction], TestFunction], TestFunction]:
        """
        Runs a test encoded into a function. Completing the function's execution counts as a
        test success; tripped assertions and other exceptions generate some other Result;
        and the test result is retained by this Suite instance.

        This decorator can be used two ways. Without application, one can decorate a
        test function without parameter:

            @suite.test
            def this_is_my_test():
                # Test goes here!

        The name of the test corresponds to that of the function. Applying the decorator can
        supply arguments to the test function and override the name of the test.

            @suite.test(name="My test, with spaces", args=(3, 4))
            def fn_test(a, b):
                # Test goes here!

        To run a test with multiple parameter sets, one may even call this function directly,
        not as a decorator:

            def fn_test(a, b):
                # Test test test...

            for a, b in [(2, 8), (3, 4)]:
                suite.test(fn_test, name=f"Test with {a}, {b}", args=(a, b))

        fn
            Function that embodies the test code.
        name
            Name of the test; by default, the name of the function is used.
        args
            Positional arguments to pass to the function to run the test.
        kwargs
            Named arguments to pass to the function to run the test.
        """
        if fn is None:
            return lambda fn: self.test(fn, name=name, args=args, kwargs=kwargs)

        try:
            fn(*args, **kwargs)
            result = Success()
        except TestFailed as err:
            result = Failure(err.reason or "Test marked as failed.", self._fns_common)
        except AssertionError as err:
            result = Failure(str(err) or "Assertion failed.", self._fns_common)
        except BaseException:
            result = Error(self._fns_common)

        name_test = name
        if not name_test:
            name_test = fn.__name__
            if args or kwargs:
                str_args = ", ".join(
                    [repr(str(a)) for a in args] +
                    [f"{k}={repr(str(v))}" for k, v in kwargs.items()]
                )
                name_test += f"({str_args})"
        self._tests.setdefault(name_test, []).append(result)
        for subscriber in self._subscribers:
            subscriber.on_result(name_test, result)

        return fn

    @staticmethod
    def _run_cell_test(cell: str) -> None:
        """
        Helper function for running tests written into cells.
        """
        code_source = "\n" + cell
        ipython = get_ipython()
        name_cell = ipython.compile.cache(code_source)
        code = compile(code_source, name_cell, "exec")
        exec(code, ipython.user_global_ns, ipython.user_ns)

    def _test_cell(self, line: str, cell: Optional[str]) -> None:
        """
        Runs a test written using a cell magic.
        """
        line = line.strip()
        if not line:
            raise ValueError("Please provide a title for the test (right after the cell magic invocation).")
        cell = (cell or "").strip()
        if not cell:
            raise ValueError("There is no test to execute! Please write some code in there.")

        self.test(self._run_cell_test, name=line, args=(cell,))

    @property
    def results(self) -> Iterator[Tuple[str, Iterator[Result]]]:
        """
        Iterates through the gathered test results. For each named test, yields a tuple of
        the name of the test and an iterator over each result gathered as the test has
        been run.
        """
        for name, test_results in self._tests.items():
            yield name, iter(test_results)

    def as_dict(self) -> Dict[str, List[Dict]]:
        "Provides a structured data representation suitable for data serialization and exportation."
        return {name: [r.as_dict() for r in rez] for name, rez in self.results}

    def __or__(self, subscriber: Subscriber) -> "Suite":
        """
        Generates a clone of this suite instance, but with this subscriber subscribed to it.

        The new suite will not share member data structures with `self`, but if `self` carries
        test results already, the new suite will reference the same result objects -- we
        assume that Result objects are immutable.
        """
        suite_with_subscriber = Suite()
        suite_with_subscriber._tests = copy(self._tests)  # Under assumption of results immutability.
        suite_with_subscriber._subscribers = copy(self._subscribers)
        suite_with_subscriber._subscribers.append(subscriber)
        return suite_with_subscriber

class Emphasis(ABC):

    @abstractmethod
    def __call__(self, s: str) -> str:
        raise NotImplementedError()

class Color(Emphasis):

    def __init__(self, fg=None, bg=None, style=None) -> None:
        super().__init__()
        self._fg = fg
        self._bg = bg
        self._style = style

    def __call__(self, s: str) -> str:
        return colors.color(s, fg=self._fg, bg=self._bg, style=self._style)

class Plain(Emphasis):

    def __call__(self, s: str) -> str:
        return s

class Colorizer:

    def __init__(self, important: Emphasis, trivial: Emphasis, failure: Emphasis, error: Emphasis) -> None:
        self.important: Emphasis = important
        self.trivial: Emphasis = trivial
        self.failure: Emphasis = failure
        self.error: Emphasis = error

def plain() -> Colorizer:
    return Colorizer(Plain(), Plain(), Plain(), Plain())

def color(  # noqa
    important: Optional[Emphasis] = None,
    trivial: Optional[Emphasis] = None,
    failure: Optional[Emphasis] = None,
    error: Optional[Emphasis] = None
) -> Colorizer:
    return Colorizer(
        important or Color(style="bold"),
        trivial or Color(fg="white"),
        failure or Color(fg="yellow"),
        error or Color(fg="red")
    )

class ProblemsEncountered(Exception):
    """Raised (optionally) when a reporting routine must report failures and errors."""

    def __init__(self, num_failures, num_errors):
        plural_failure = "s" if num_failures > 1 else ""
        plural_errors = "s" if num_errors > 1 else ""
        super().__init__(
            f"Problems encountered during testing: {num_failures} failure{plural_failure}, "
            f"{num_errors} error{plural_errors}"
        )
        self.num_failures = num_failures
        self.num_errors = num_errors

def raise_on_error(suite: Suite) -> None:
    num_failures = 0
    num_errors = 0
    for _, rez in suite.results:
        for r in rez:
            if not r.is_success():
                if r.is_failure():
                    num_failures += 1
                else:
                    num_errors += 1
    if num_failures > 0 or num_errors > 0:
        raise ProblemsEncountered(num_failures, num_errors)

TestNameFormatter = Callable[[str, int], str]


def name_all(name_test: str, num_result: int) -> str:
    """
    Test name formatter that puts out the name of a test even when it has
    been run multiple times.
    """
    return name_test


def ladder(name_test: str, num_result: int) -> str:
    """
    Test name formatter that puts out the name of a test only once, even
    if it has been run multiple times.
    """
    if num_result == 0:
        return name_test
    return " " * len(name_test)

def quoter(formatter: TestNameFormatter) -> TestNameFormatter:
    """
    Test name formatter that surrounds the name between double quotes. Not
    meant to be used directly by users of this module.
    """
    def quoter_format(name_test: str, num_result: int) -> str:
        return f"\"{formatter(name_test, num_result)}\""

    return quoter_format

class PolicyReportingProblems:
    """What to do when reporting test results that involve problems (failures and errors)."""
    def __init__(self, label: str) -> None:
        self.label = label

    def __str__(self) -> str:
        return self.label

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PolicyReportingProblems):
            return False
        return self.label == other.label


IGNORE = PolicyReportingProblems("ignore")
RAISE = PolicyReportingProblems("raise")

def report_results(  # noqa
    suite: Suite,
    file: TextIOBase = sys.stdout,
    colorizer: Colorizer = color(),
    format_name_test: TestNameFormatter = ladder,
    sep_name_result: str = "\t",
    quote_names: bool = False,
    labels_result_custom: Mapping[type, str] = {},
    on_error: PolicyReportingProblems = IGNORE
) -> None:
    """
    Reports the name and result for each attempt at running a test, without details
    as to issues encountered (failures and errors).

    suite
        Suite of test to write report from.
    file
        File-like object to write report to. Default is standard output.
    colorizer
        Policy for emphasizing the written report.
    format_name_test
        Some tests are run more than once (for instance, for iterative problem solving).
        In a report written for human reading, the repeated naming of a test run more
        than once can feel redundant; it is eliminated by setting this to `ladder`.
        All tests will be named if the formatter used instead is `name_all`.
    sep_name_result
        Separating character used between test name and result label. Default is "\t".
    quote_names
        If True, the test names will be surrounded with double quotes in the output.
    labels_result_custom
        Dictionary of labels to use with different result types, when the default
        labels (*ok* for success, *failed* for failure, *ERROR* for error) should be
        changed. The emphasis for each label is derived from the colorizer.
    on_error
        What to do when reporting results that include problems such as failures and
        errors. If set to RAISE, it will raise a ProblemsEncountered exception, which
        is useful when running the notebook as part of a CI/CD pipeline; otherwise,
        or if set to IGNORE, nothing more is done than writing the report.
        Default is IGNORE.
    """
    len_all_names = [len(name) for name, _ in suite.results]
    if len(len_all_names) == 0:
        return
    len_name_largest = max(len_all_names)

    labels_result = {
        type_result: colorize(labels_result_custom.get(type_result, label_default))
        for type_result, colorize, label_default in [
            (Success, Plain(), "ok"),
            (Failure, colorizer.failure, "failed"),
            (Error, colorizer.error, "ERROR")
        ]
    }

    if quote_names:
        format_name_test = quoter(format_name_test)

    for name, rez in suite.results:
        p_name = f"{name:{len_name_largest}s}"
        for num, r in enumerate(rez):
            print(format_name_test(p_name, num), labels_result[type(r)], sep=sep_name_result, file=file)

    if on_error is RAISE:
        raise_on_error(suite)

def summarize_results(  # noqa
    suite: Suite,
    file: Optional[TextIOBase] = sys.stdout,
    colorizer: Colorizer = color(),
    sep: str = ", ",
    on_error: PolicyReportingProblems = IGNORE
) -> Dict[type, int]:
    """
    Writes a very short summary of a test run, counting the number of each result obtained.

    suite
        Suite of test to write report from.
    file
        File-like object to write report to. Default is standard output.
    colorizer
        Policy for emphasizing the written report.
    sep
        Separation string between the labeled numbers of results. Default is ", "
    on_error
        What to do when reporting results that include problems such as failures and
        errors. If set to RAISE, it will raise a ProblemsEncountered exception, which
        is useful when running the notebook as part of a CI/CD pipeline; otherwise,
        or if set to IGNORE, nothing more is done than writing the report.
        Default is IGNORE.
    """
    summary = {t: 0 for t in [Success, Failure, Error]}
    for _, rez in suite.results:
        for r in rez:
            summary[type(r)] += 1

    if file is not None:
        print(
            f"{summary[Success]} passed",
            (colorizer.failure if summary[Failure] > 0 else colorizer.trivial)(f"{summary[Failure]} failed"),
            (colorizer.error if summary[Error] > 0 else colorizer.trivial)(f"{summary[Error]} raised an error"),
            file=file,
            sep=sep
        )

    if on_error == RAISE:
        raise_on_error(suite)
    return summary

def print_frame(  # noqa
    frame: Frame,
    file: TextIOBase = sys.stdout,
    colorizer: Colorizer = color(),
    lines_context: int = 3
) -> None:
    """
    Writes up a single stack frame report.

    frame
        Stack frame to report on.
    file
        File-like object to write report to. Default is standard output.
    colorizer
        Policy for emphasizing the written report.
    lines_context
        Number of lines of code to fetch and write up before and after the
        line associated to the stack frame.
    """
    header = (
        colorizer.trivial
        if Error.TAG_COMMON in frame.tags
        else Plain()
    )(
        " | ".join([
            "Code cell" if "cell" == frame.name_file else f"File {frame.name_file}",
            f"Line {frame.num_line}",
            f"Function {frame.function}"
        ])
    )
    print(header, file=file)
    if Error.TAG_COMMON not in frame.tags:
        context: List[Tuple[int, str]] = frame.context(before=lines_context, after=lines_context)
        if len(context) > 0:
            max_len_num_line = len(str(context[-1][0]))
            for i, line in zip(
                [i for i, _ in context],
                highlight(
                    "\n".join(ln for _, ln in context),
                    lexer=Python3Lexer(),
                    formatter=TerminalFormatter()
                ).split("\n")
            ):
                print(
                    colorizer.trivial(f"{i:{max_len_num_line}d}"),
                    colorizer.trivial("|"),
                    line,
                    sep=" ",
                    file=file
                )
    print(file=file)

def detail_result(  # noqa
    name_test: str,
    result: Error,
    prefix_header: str,
    file: TextIOBase = sys.stdout,
    colorizer: Colorizer = color(),
    lines_context: int = 3
) -> None:
    """
    Writes up a report regarding a single test result.

    name_test
        Name of the test the result was gotten for.
    result
        Error-type result to report on.
    prefix_header
        String prepended to the header of the result report.
    file
        File-like object to write report to. Default is standard output.
    colorizer
        Policy for emphasizing the written report.
    lines_context
        Number of lines of code to fetch and write up before and after the
        line associated to the stack frame.
    """
    header = " ** ".join([
        prefix_header,
        f"Test {colorizer.important(name_test)}",
        {Failure: colorizer.failure, Error: colorizer.error}[type(result)](type(result).__name__)
    ])
    print("-" * len(colors.strip_color(header)), file=file)
    print(header, file=file)
    if result.is_failure():
        print(result.reason, file=file)
    else:
        print(f"{result.type_exc.__name__}:", str(result.value_exc) or "<no detail provided>", file=file)
    print(file=file)

    for frame in result.traceback:  # First frame is always Suite.test, which is irrelevant.
        print_frame(frame, file=file, colorizer=colorizer, lines_context=lines_context)

def detail_issues(  # noqa
    suite: Suite,
    file: TextIOBase = sys.stdout,
    colorizer: Colorizer = color(),
    lines_context: int = 3,
    max_report: int = sys.maxsize,
    on_error: PolicyReportingProblems = IGNORE
) -> None:
    """
    Writes up a report detailing the issues encountered while running the test suite.

    suite
        The test suite.
    file
        The file-like object to write the report to. Default is standard output.
    colorizer
        Color scheme used for emphasizing the various bits of the report.
    lines_context
        Number of lines of context to provide around each line of code involved
        in a reported problem.
    max_report
        Maximum number of problems to report on.
    on_error
        What to do when reporting results that include problems such as failures and
        errors. If set to RAISE, it will raise a ProblemsEncountered exception, which
        is useful when running the notebook as part of a CI/CD pipeline; otherwise,
        or if set to IGNORE, nothing more is done than writing the report.
        Default is IGNORE.
    """
    summary = summarize_results(suite, file=None)
    num_problems = summary[Failure] + summary[Error]
    num_remaining: int = -1
    if num_problems == 0:
        if summary[Success] == 0:
            print("No test run.", file=file)
        else:
            print(f"All {summary[Success]} tests passed. No failure nor error encountered.", file=file)
    else:
        index = 1
        for name, rez in suite.results:
            if num_remaining < 0:
                for r in rez:
                    if not r.is_success():
                        detail_result(name, r, f"# {index}/{num_problems}", lines_context=lines_context, file=file)
                        print()

                        if index >= max_report:
                            num_remaining = num_problems - index
                            break
                        index += 1

    if num_remaining > 0:
        print(
            colorizer.important(
                f"... plus {num_remaining} other issue{'s' if num_remaining > 1 else ''}."
            ),
            file=file
        )
    if on_error == RAISE:
        raise_on_error(suite)

class Report(Subscriber):
    """
    Test suite subscriber that reports on test results on-the-fly. When a test
    does not succeed, details on the failure can optionally be provided. See
    documentation on class `Suite` to get an example on the usage of this
    plug-in.

    file
        File-like object where the test results are reported. Default is
        standard output.
    verbose
        If True, the feedback on test results contains traceback information
        when problems are encountered.
    file
        File-like object where the feedback is put out.
    colorizer
        Policy on how to emphasize the feedback output.
    lines_context
        Number of lines of code to provide as context in traceback frames
        around the line of code at the nexus of an issue.
    """
    def __init__(
        self,
        verbose: bool = True,
        file: TextIOBase = sys.stdout,
        colorizer: Colorizer = color(),
        lines_context: int = 3
    ) -> None:
        super().__init__()
        self._last: Optional[bool] = None
        self._file = file
        self._verbose = verbose
        self._colorizer = colorizer
        self._lines_context = lines_context

    def on_result(self, name_test: str, result: Result) -> None:
        name_test = self._colorizer.important(name_test)
        if result.is_success():
            msg = f"Test {name_test} passed."
            if self._verbose and self._last is False:
                print("-" * len(colors.strip_color(msg)), file=self._file)
            self._last = True
            print(msg, file=self._file)
        else:
            if self._last is True:
                print(file=self._file)
            self._last = False
            if self._verbose:
                detail_result(
                    name_test,
                    result,
                    "Issue encountered",
                    self._file,
                    self._colorizer,
                    self._lines_context
                )
            else:
                index_frame_relevant = -1
                if result.is_failure():
                    label = self._colorizer.failure(f"Test {name_test} failed")
                    print(f"{label}: {result.reason}", file=self._file)
                    if isinstance(result.type_exc, TestFailed):
                        index_frame_relevant = -2
                else:
                    label = self._colorizer.error(f"Error occured during test {name_test}")
                    value_exc = ""
                    if str(result.value_exc):
                        value_exc = f" -- {str(result.value_exc)}"
                    print(f"{label}: {result.type_exc.__name__}{value_exc}", file=self._file)
                frame_relevant = result.traceback[index_frame_relevant]
                print_frame(
                    frame_relevant,
                    file=self._file,
                    colorizer=self._colorizer,
                    lines_context=self._lines_context
                )