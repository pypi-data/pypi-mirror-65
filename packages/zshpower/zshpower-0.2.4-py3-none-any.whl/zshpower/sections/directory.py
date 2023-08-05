import os
from pathlib import Path
from .lib.utils import Color, abspath_link
from .lib.utils import choice_symbol, prefix_text_formatting


def shorten_path(file_path, length):
    return Path(*Path(file_path).parts[-length:])


class Directory(Color):
    def __init__(self, config):
        super().__init__()
        self.username_enable = config["username"]["enable"]
        self.hostname_enable = config["hostname"]["enable"]
        self.directory_truncate_value = config["directory"]["truncation_length"]
        self.directory_symbol = choice_symbol(config["directory"]["symbol"], "")
        self.directory_color = config["directory"]["color"]
        self.directory_prefix_color = config["directory"]["prefix"]["color"]
        self.directory_prefix_text = prefix_text_formatting(config["directory"]["prefix"]["text"])

    def __str__(self, prefix="", space_elem=" "):
        if (
            self.username_enable
            or os.geteuid() == 0
            or self.hostname_enable
            or "SSH_CONNECTION" in os.environ
        ):
            prefix = (
                f"{Color(self.directory_prefix_color)}"
                f"{self.directory_prefix_text}{Color().NONE}"
            )

        directory = shorten_path(abspath_link(), int(self.directory_truncate_value))
        if (
            str(directory) == str(Path.home())
            or str(directory) == str(Path.home())[1:]
            or str(directory) == str(Path.home()).split("/")[2].strip()
        ):
            directory = "~"

        directory_export = (
            f"{prefix}{Color(self.directory_color)}{self.directory_symbol}"
            f"{directory}{space_elem}{Color().NONE}"
        )

        return str(directory_export)
