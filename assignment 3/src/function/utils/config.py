import numpy


class Config:
    """
    function class for managing config

        Attributes
        ----------
        dict_config : dict
            dictionary of the config file

        Methods
        -------
        get_config(key)
            returns the value of the key
        set_config(key, value)
            sets the value of the key
    """

    def __init__(self, dict_config):
        self.config = dict_config

    def get_config(self, key):
        return self.config[key]

    def set_config(self, key, value):
        self.config[key] = value
