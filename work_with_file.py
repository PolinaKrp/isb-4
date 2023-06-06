import logging
import json
import csv


def read_settings(settings: str) -> dict:
    """the function reads values from settings.json"""
    try:
        with open(settings) as json_file:
            settings = json.load(json_file)
        logging.info(
            f"the data of settings successfully read")
    except Exception as e:
        logging.warning(
            f"an error occurred when reading data to '{settings}' file: {str(e)}")
    return settings


def write_settings(settings: dict, path_settings: str) -> None:
    """the function writes values to settings.json"""
    try:
        with open(path_settings, 'w') as f:
            json.dump(settings, f)
        logging.info(
            f"the data of settings successfully write")
    except Exception as e:
        logging.warning(
            f"an error occurred when writing data to '{settings}' file: {str(e)}")
