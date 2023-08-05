"""
Optical cavity parameter calculator.

This is primarily a program to be used from the command line (see
:ref:`command_line`) but can also be used programmatically through the
recommended single function interface :func:`cavcalc.calculate` (see
:ref:`module` for more details).
"""

import configparser
import os
import shutil

try:
    from .version import version as __version__
except ImportError:
    __version__ = "?.?.?"


def __get_config_path():
    return os.path.join(
        os.environ.get("APPDATA")
        or os.environ.get("XDG_CONFIG_HOME")
        or os.path.join(os.environ["HOME"], ".config"),
        "cavcalc",
    )


def __write_config_file():
    configpath = __get_config_path()

    os.makedirs(configpath, exist_ok=True)

    default_ini_file = os.path.join(os.path.dirname(__file__), "cavcalc.ini")
    if not os.path.exists(default_ini_file):
        __generate_default_config_file()

    usr_ini_file = os.path.join(configpath, "cavcalc.ini")
    if not os.path.exists(usr_ini_file):
        shutil.copyfile(default_ini_file, usr_ini_file)


def __read_config_file():
    config = configparser.ConfigParser()

    # try to read in a config file from current working directory first
    if os.path.isfile("cavcalc.ini"):
        config.read("cavcalc.ini")

    # then try to read from user's default config directory
    else:
        configpath = __get_config_path()

        usr_ini_file = os.path.join(configpath, "cavcalc.ini")
        if os.path.exists(usr_ini_file):
            config.read(usr_ini_file)

        # finally get the config file within the package itself
        else:
            default_ini_file = os.path.join(os.path.dirname(__file__), "cavcalc.ini")

            if os.path.exists(default_ini_file):
                config.read(default_ini_file)
            else:
                config = __generate_default_config_file(write=False)

    return config


def __generate_default_config_file(write=True):
    config = configparser.ConfigParser()

    config["plotting"] = {"matplotlib_backend": "", "style": ""}
    config["bug reporting"] = {"report": False}
    config["units"] = {
        "length": "m",
        "towaist": "m",
        "curvature": "m",
        "beamsize": "cm",
        "gouy": "deg",
        "divergence": "deg",
        "frequency": "Hz",
    }

    if write:
        path = os.path.join(os.path.dirname(__file__), "cavcalc.ini")
        with open(path, "w") as configfile:
            config.write(configfile)

    return config


def __check_config_file(config):
    from .utilities import quit_print

    # plotting section
    if "plotting" not in config:
        print(
            "WARNING: No [plotting] section in cavcalc config file. This may lead to errors."
        )
    else:
        plotting_sec = config["plotting"]
        style = plotting_sec.get("style", "")
        if style and not os.path.isfile(style):
            quit_print(
                "ERROR: The style option specified in the [plotting] section "
                "of the cavcalc config file does not point to a valid file location."
            )

    # bug report section
    if "bug reporting" not in config:
        print(
            "WARNING: No [bug reporting] section in cavcalc config file. This may lead to errors."
        )
    else:
        bug_reporting_sec = config["bug reporting"]
        report = bug_reporting_sec.get("report", "")
        if report.casefold() not in (
            "1",
            "yes",
            "true",
            "on",
            "0",
            "no",
            "false",
            "off",
        ):
            quit_print(
                "ERROR: The report option specified in the [bug reporting] section "
                "of the cavcalc config file cannot be coerced to a boolean value."
            )

    # units section
    if "units" not in config:
        print(
            "WARNING: No [units] section in cavcalc config file. This may lead to errors."
        )
    else:
        distance_units = ["pm", "nm", "um", "mm", "cm", "m", "km"]
        frequency_units = ["pHz", "nHz", "uHz", "mHz", "Hz", "kHz", "MHz", "GHz", "THz"]
        angular_units = ["deg", "degrees", "rad", "rads", "radians"]

        units_sec = config["units"]

        invalids = []
        length = units_sec.get("length", "")
        if length not in distance_units:
            invalids.append("length")
        towaist = units_sec.get("towaist", "")
        if towaist not in distance_units:
            invalids.append("towaist")
        curvature = units_sec.get("curvature", "")
        if curvature not in distance_units:
            invalids.append("curvature")
        beamsize = units_sec.get("beamsize", "")
        if beamsize not in distance_units:
            invalids.append("beamsize")

        gouy = units_sec.get("gouy", "")
        if gouy.casefold() not in angular_units:
            invalids.append("gouy")
        divergence = units_sec.get("divergence", "")
        if divergence.casefold() not in angular_units:
            invalids.append("divergence")

        frequency = units_sec.get("frequency", "")
        if frequency not in frequency_units:
            invalids.append("frequency")

        if invalids:
            quit_print(
                f"ERROR: The values of the following options: {invalids} specified in the [units] "
                "section of the cavcalc config file are invalid."
            )


__write_config_file()
CONFIG = __read_config_file()
__check_config_file(CONFIG)

from .calculate import calculate
from .parameter import Parameter
