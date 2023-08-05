from .ATPKeywords import ATPKeywords
from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    pass

class ATPLibrary(ATPKeywords):
    """``ATPLibrary`` is a ATP keyword library that uses
    test library that uses the [https://github.com/kennethreitz/requests|Requests] HTTP client.
    Here is a sample test case:
    | ***** Settings *****   |                                 |                     |                       |               |
    | Library                | Collections                     |                     |                       |               |
    | Library                | ATPLibrary                      |                     |                       |               |
    | ***** Test Cases ***** |                                 |                     |                       |               |
    | Till Transaction       |                                 |                     |                       |               |
    |                        | Perform Ping                    |                     |                       |               |
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'