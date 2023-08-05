"""
Implementation of the TestResult CFX Enumeration.

Supports a bool override for ease of use.
"""
from .base import CFXEnum


class TestResult(CFXEnum):
    """The result of a test.

    Passed: The test passed
    Failed: The test failed
    Error: The test could not be completed because an error occurred.
    Aborted: The test was aborted by the operator / user.
    """
    Passed = 0
    Failed = 1
    Error = 2
    Aborted = 3

    def __bool__(self):
        return self.value == 0  # pylint: disable=comparison-with-callable;
