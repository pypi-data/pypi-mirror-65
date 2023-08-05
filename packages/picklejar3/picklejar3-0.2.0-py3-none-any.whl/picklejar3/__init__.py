__author__ = "Kevin Walchko"
__license__ = "MIT"

try:
    from importlib.metadata import version # type: ignore
except ImportError:
    from importlib_metadata import version # type: ignore

__version__ = version("picklejar3")
