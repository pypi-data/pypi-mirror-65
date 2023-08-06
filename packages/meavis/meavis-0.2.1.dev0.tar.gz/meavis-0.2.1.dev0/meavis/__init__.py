"""Measurement & Visualisation python framework."""

import logging
import logging.config
import os
import shutil

import yaml
from pkg_resources import get_distribution


__version__ = get_distribution(__name__).version

__title__ = "MeaVis"
__description__ = "Measurement & Visualisation python framework."
__uri__ = "https://gitlab.com/fblanchet/meavis"

__author__ = "Hofheinz' group"
__email__ = "florian.blanchet@supoptique.org"
__license__ = "Apache"
__copyright__ = "2020 Hofheinz' group"


logging_conf_dir = os.path.expanduser(os.path.join("~", ".config", "meavis"))
if not os.path.exists(logging_conf_dir):
    os.makedirs(logging_conf_dir)
logging_conf_path = os.path.join(logging_conf_dir, "logging.conf")
if not os.path.exists(logging_conf_path):
    shutil.copy2(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "logging.conf"
        ),
        logging_conf_path,
    )

with open(logging_conf_path) as file:
    log_conf = yaml.safe_load(file)
    log_conf["handlers"]["file_short"]["filename"] = os.path.join(
        logging_conf_dir, log_conf["handlers"]["file_short"]["filename"]
    )
    log_conf["handlers"]["file_long"]["filename"] = os.path.join(
        logging_conf_dir, log_conf["handlers"]["file_long"]["filename"]
    )
    logging.config.dictConfig(log_conf)

del logging_conf_dir
del logging_conf_path
