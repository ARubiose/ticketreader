"""Configuration file for ticketreader app."""
import pathlib
import logging.config

ROOT_DIR = pathlib.Path(__file__).parents[1]
DATA_DIR = ROOT_DIR / "data"
CONFIG_DIR = ROOT_DIR / "config"
# Logging
logging.config.fileConfig(CONFIG_DIR / "logging.ini")
