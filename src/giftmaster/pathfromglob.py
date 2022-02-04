import logging
import os
import pathlib


class NonRelativeGlob:
    """
    >>> import pathlib
    >>> import os
    >>>
    >>> _str = r"C:\Program*\WiX Toolset*\bin\heat.exe"
    >>> p1 = pathlib.Path(_str)
    >>> x = str(p1).lstrip(p1.drive)
    >>> x = str(x).lstrip(p1.root)
    >>> root = pathlib.Path("/")
    >>> z = f"*{x}"
    >>> print(z)
    *Program*\WiX Toolset*\bin\heat.exe
    >>> os.chdir("c:")
    >>> y = pathlib.Path("/").glob(z)
    >>> print(y)
    <generator object Path.glob at 0x0000026FE9F96820>
    >>> print(list(y))
    [WindowsPath('/Program Files (x86)/WiX Toolset v3.11/bin/heat.exe')]
    >>>"""

    def __init__(self, _str):
        self.logger = logging.getLogger(__name__)
        self.glob = None
        self.cwd = pathlib.Path.cwd()
        self.ps = _str
        self.drive = pathlib.Path(_str).drive
        self.path = None
        self.initialize(_str)

    def initialize(self, _str):
        try:
            p1 = pathlib.Path(self.ps)
            self.logger.debug(p1)
            x = str(p1).lstrip(p1.drive)
            self.logger.debug(x)
            x = str(x).lstrip(p1.root)
            self.logger.debug(x)
            root = pathlib.Path("/")
            z = f"*{x}"
            self.logger.debug(z)
            if self.drive:
                os.chdir(p1.drive)
            self.logger.debug(pathlib.Path.cwd())
            y = pathlib.Path("/").glob(z)  # y is a generator
            self.logger.debug(y)
            paths = list(y)  # consumes the generator
            self.logger.debug(paths)
            if not paths:
                self.logger.warning("couldn't find a match for {}".format(self.ps))
            else:
                # naively choose one with higest version number
                last = paths[-1]
                last = last.resolve()
                self.logger.debug("using file with path {}".format(last))
                self.path = last

        except BaseException as ex:
            self.logger.exception(ex)
            raise

        finally:
            os.chdir(self.cwd)


class PathFromGlob:
    """
    # multiline string like this

    C:/Program*/Microsoft SDKs/Windows/v[!6]*/Bin/SignTool.exe
    C:/Program*/Windows Kits/*/bin/*/*/SignTool.exe

    or single glob like this:
    C:/Program*/Windows Kits/*/bin/*/*/SignTool.exe
    */Program*/Windows Kits/*/bin/*/*/SignTool.exe
    """

    def __init__(self, _str):
        self.logger = logging.getLogger(__name__)
        self.root = None
        self.globs_str = _str
        self.path = None
        self.initialize(_str)

    def clean(self, line):
        return line.strip()

    def initialize(self, _str):
        self.logger.debug(self.globs_str)

        candidates = []
        for line in _str.splitlines():
            self.logger.debug("line:{}".format(line))
            clean = self.clean(line)
            self.logger.debug("path:{}".format(clean))
            if not clean:
                continue
            nrg = NonRelativeGlob(clean)
            self.logger.debug(nrg.path)
            if nrg.path:
                candidates.append(nrg.path)

        if candidates:
            self.path = candidates[-1]

    @classmethod
    def from_string(cls, _str):
        return cls(_str)
