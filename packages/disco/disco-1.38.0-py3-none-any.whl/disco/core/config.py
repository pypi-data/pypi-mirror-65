import json

from disco.core import constants


class Config:
    """
    Handles local configuraion values
    """

    def __init__(self):
        if constants.DISCO_CONFIG_PATH.exists():
            self.config = json.loads(constants.DISCO_CONFIG_PATH.read_text())
        else:
            self.config = {}

    def get(self, key):
        """
        Get a config item
        Args:
            key: key for the config item

        Returns: value of config item
        """
        return self.config.get(key)

    def set(self, key, value):
        """
        Sets a config item and saves it
        Args:
            key: the item key
            value: the item value
        """
        if key in self.config and self.config[key] == value:
            return
        self.config[key] = value
        self._save_config()

    def reset(self, key):
        """
        Delete the item from config
        Args:
            key: key for the item
        """
        self.config.pop(key, None)
        self._save_config()

    def _save_config(self):
        """
        private function for saving the config to file
        """
        json_content = json.dumps(self.config)
        constants.DISCO_CONFIG_PATH.write_text(json_content)
