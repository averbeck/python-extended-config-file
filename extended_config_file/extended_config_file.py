import configparser

from abc import ABC, abstractmethod
from pathlib import Path


class ExtendedConfigInterface(ABC):
    @abstractmethod
    def save_config(self, pathConfigFullFileName: Path | None = None):
        raise NotImplementedError

    @abstractmethod
    def ensure_entry(self, strSection: str, strEntry: str, strValue: str | None = None):
        raise NotImplementedError

    @abstractmethod
    def add_entry(self, strSection: str, strEntry: str, strValue: str | None = None):
        raise NotImplementedError


class ExtendedConfig(configparser.ConfigParser, ExtendedConfigInterface):
    def __init__(
        self, pathConfigFullFileName: Path | None = None, allow_no_value=False
    ):
        super().__init__(allow_no_value=True)

        self.pathConfigFullFileName: Path = (
            pathConfigFullFileName if pathConfigFullFileName else Path("settings.ini")
        )
        self._bConfigNeedsRewrite: bool = False
        self.parent: ExtendedConfig | None = None

        try:
            self.load_config()
        except FileNotFoundError() as err:
            if not allow_no_value:
                raise err

    def load_config(self):
        self.read(str(self.pathConfigFullFileName))

        # Cleanup
        for strSection in self:
            for strEntry in self[strSection]:
                if strEntry.startswith("#") or strEntry.startswith(";"):
                    del self[strSection][strEntry]

        return self

    def save_config(self, pathConfigFullFileName: Path | None = None):
        if not self._bConfigNeedsRewrite:
            return

        if pathConfigFullFileName is None:
            pathConfigFullFileName = self.pathConfigFullFileName

        with pathConfigFullFileName.open("w") as fpConfigFile:
            self.write(fpConfigFile)

    def ensure_entry(self, strSection: str, strEntry: str, strValue: str | None = None):
        if strSection not in self:
            self[strSection] = {}

        if strEntry not in self[strSection]:
            self._bConfigNeedsRewrite = True
            self.set(strSection, strEntry, strValue)

    def add_entry(self, strSection: str, strEntry: str, strValue: str | None = None):
        if strSection not in self:
            self[strSection] = {}

        self._bConfigNeedsRewrite = True
        self.set(strSection, strEntry, strValue)

    def section(self, strSectionName: str) -> "ExtendedConfigSection":
        configSection = ExtendedConfigSection(strSectionName, parent=self)

        return configSection


class ExtendedConfigSection(dict, ExtendedConfigInterface):
    def __init__(self, strSectionKey: str, parent: ExtendedConfig):
        super().__init__()

        self.strSectionKey: str = strSectionKey
        self._parent: ExtendedConfig = parent

        for key, value in self._parent.items(self.strSectionKey):
            self[key] = value

    def save_config(self, pathConfigFullFileName: Path | None = None):
        return self._parent.save_config(pathConfigFullFileName)

    def ensure_entry(self, strEntry: str, strValue: str | None = None):
        return self._parent.ensure_entry(self.strSectionKey, strEntry, strValue)
