import os
import sys

import yaml


class GlobalParams(dict):
    """
    This is a class for managing the global params from a config yml file.
    """

    def __init__(self):
        """
        The constructor for the GlobalParams class.
        """
        super().__init__()
        self.update(self.get_yml_file())

    @staticmethod
    def get_yml_file() -> dict:
        """
        Opens a yaml file from sys.argv[-1].

        :return: (dict) data from yaml file
        """
        if os.environ.get("FLASK_ENV") is not None and os.environ.get("FLASK_ENV") == "production":
            file_name = "secret_config.yml"
        else:
            file_name = sys.argv[-1]
            if ".yml" not in file_name:
                file_name = "config.yml"

        if os.path.isfile(file_name):
            with open("./{}".format(file_name)) as file:
                data = yaml.load(file, Loader=yaml.FullLoader)
            return data
        raise ValueError("{} config file is not available".format(file_name))

    def _override_sqlite(self) -> None:
        """
        Overwrites the database URL to local SQLite.

        :return: None
        """
        if os.environ.get("SQLITE") is not None:
            self["DB_URL"] = 'sqlite:///dev.db'
