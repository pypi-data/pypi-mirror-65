from snakypy.console import cmd as cmd_snakypy
from snakypy.path import create as snakypy_path_create
from snakypy.file import create as snakypy_file_create
from os import remove as os_remove
from datetime import datetime
from re import sub as re_sub, M as re_m
from shutil import copyfile as shutil_copyfile
from zipfile import ZipFile
from os.path import join, exists, isdir, isfile
from sys import platform
from tomlkit import parse as toml_parse, dumps as toml_dumps
from snakypy import printer, FG
from zshpower.utils.catch import read_zshrc, plugins_current_zshrc


def create_config(content, file_path, force=False):
    if not exists(file_path) or force:
        parsed_toml = toml_parse(content)
        write_toml = toml_dumps(parsed_toml)
        snakypy_file_create(write_toml, file_path, force=force)
        return True
    return


def create_zshrc(content_, zsh_rc):
    if exists(zsh_rc):
        if not read_zshrc(zsh_rc):
            shutil_copyfile(zsh_rc, f"{zsh_rc}-D{datetime.today().isoformat()}")
            snakypy_file_create(content_, zsh_rc, force=True)
            return True
    elif not exists(zsh_rc):
        snakypy_file_create(content_, zsh_rc)
        return True
    return


def change_theme_in_zshrc(zsh_rc, theme_name):
    if read_zshrc(zsh_rc):
        current_theme = read_zshrc(zsh_rc)[2]
        new_theme = f'ZSH_THEME="{theme_name}"'
        new_zsh_rc = re_sub(
            rf"{current_theme}", new_theme, read_zshrc(zsh_rc)[1], flags=re_m
        )
        snakypy_file_create(new_zsh_rc, zsh_rc, force=True)
        return True
    return


def omz_install(omz_root):
    omz_github = "https://github.com/ohmyzsh/ohmyzsh.git"
    cmd_line = f"git clone {omz_github} {omz_root}"
    try:
        if not exists(omz_root):
            printer("Install Oh My ZSH...", foreground=FG.QUESTION)
            cmd_snakypy(cmd_line, verbose=True)
            printer(
                "Oh My ZSH installation process finished.", foreground=FG.FINISH,
            )

    except Exception:
        raise Exception("Error downloading Oh My ZSH. Aborted!")


def omz_install_plugins(omz_root, plugins):
    try:
        url_master = "https://github.com/zsh-users"
        for plugin in plugins:
            path = join(omz_root, f"custom/plugins/{plugin}")
            clone = f"git clone {url_master}/{plugin}.git {path}"
            if not isdir(path):
                printer(f"Install plugins {plugin}...", foreground=FG.QUESTION)
                cmd_snakypy(clone, verbose=True)
                printer(f"Plugin {plugin} task finished!", foreground=FG.FINISH)
    except Exception:
        raise Exception(f"There was an error installing the plugin")


def install_fonts(home, force=False):
    url = "https://github.com/snakypy/snakypy-static"
    base_url = f"blob/master/zshpower/fonts/fonts.zip?raw=true"
    font_name = "DejaVu Sans Mono Nerd Font"
    fonts_dir = join(home, f".fonts")
    snakypy_path_create(fonts_dir)
    curl_output = join(home, "zshpower__font.zip")

    if platform.startswith("linux"):
        try:
            if (
                not isfile(join(fonts_dir, "DejaVu Sans Mono Nerd Font Complete.ttf"))
                or force
            ):
                printer(
                    f'Please wait, downloading the "{font_name}" font and'
                    "installing...",
                    foreground=FG.QUESTION,
                )
                cmd_line = f"curl -L {join(url, base_url)} -o {curl_output}"
                cmd_snakypy(cmd_line, verbose=True)

                with ZipFile(curl_output, "r") as zip_ref:
                    zip_ref.extractall(fonts_dir)
                    os_remove(curl_output)
                    printer("Done!", foreground=FG.FINISH)
                return True
            return
        except Exception as err:
            raise Exception(f'Error downloading font "{font_name}"', err)
    return


def add_plugins_zshrc(zsh_rc):
    plugins = (
        "python",
        "django",
        "pip",
        "pep8",
        "autopep8",
        "zsh-syntax-highlighting",
        "zsh-autosuggestions",
    )
    current = plugins_current_zshrc(zsh_rc)
    new_plugins = []
    for plugin in plugins:
        if plugin not in current:
            new_plugins.append(plugin)

    if len(new_plugins) > 0:
        plugins = f'plugins=({" ".join(current)} {" ".join(new_plugins)})'
        new_zsh_rc = re_sub(
            rf"^plugins=\(.*", plugins, read_zshrc(zsh_rc)[1], flags=re_m
        )
        snakypy_file_create(new_zsh_rc, zsh_rc, force=True)
        return new_zsh_rc
    return
