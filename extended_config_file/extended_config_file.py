import configparser

from pathlib import Path


class ExtendedConfigFile(configparser.ConfigParser):
    def __init__(self, pathConfigFullFileName: Path | None = None):
        super().__init__(allow_no_value=True)

        self.pathConfigFullFileName: Path = pathConfigFullFileName if pathConfigFullFileName else Path("settings.ini")
        self.bConfigNeedsRewrite: bool = False

        self.load_config()

    def load_config(self):

        self.read(str(self.pathConfigFullFileName))

        # Cleanup
        for strSection in self:
            for strEntry in self[strSection]:
                if strEntry.startswith("#") or strEntry.startswith(";"):
                    del self[strSection][strEntry]

        return self

    def save_config(self, pathConfigFullFileName: Path | None = None):

        if not self.bConfigNeedsRewrite:
            return

        if pathConfigFullFileName is None:
            pathConfigFullFileName = self.pathConfigFullFileName

        with pathConfigFullFileName.open("w") as fpConfigFile:
            self.write(fpConfigFile)

    def ensure_entry(self, strSection: str, strEntry: str, strValue: str | None = None):

        if strSection not in self:
            self[strSection] = {}

        if strEntry not in self[strSection]:
            self.bConfigNeedsRewrite = True
            self.set(strSection, strEntry, strValue)

    def add_entry(self, strSection: str, strEntry: str, strValue: str | None = None):

        if strSection not in self:
            self[strSection] = {}

        self.bConfigNeedsRewrite = True
        self.set(strSection, strEntry, strValue)
