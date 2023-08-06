try:
    from .api import TiramisuCmdlineParser
except ImportError as err:
    import warnings
    warnings.warn("cannot not import TiramisuCmdlineParser {err}", ImportWarning)
    TiramisuCmdlineParser = None

__version__ = "0.5"
__all__ = ('TiramisuCmdlineParser',)
