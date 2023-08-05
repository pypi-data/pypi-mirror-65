from .exceptions import ConfigException
from datetime import date


class AppConfig():

    toggl_config_keys = ['toggl_user', 'toggl_workspace_id',
                         'toggl_start_date', 'toggl_end_date', 'toggl_api_token']

    def __init__(self, config):
        self.config = config
        self.set_date_interval(config)
        AppConfig.__check_config_integrity(self.config)

    def set_date_interval(self, config):
        dates = ['toggl_start_date', 'toggl_end_date']
        for date_config in dates:
            if date_config in config:
                self.config[date_config] = config[date_config]
            else:
                self.config[date_config] = str(date.today())

    def get(self, config_name):
        return self.config.get(config_name)

    def set_start_date(self, date: str):
        self.config['toggl_start_date'] = date

    def toggl_config(self):
        return self.__get_config_from_keys(AppConfig.toggl_config_keys)

    def __get_config_from_keys(self, keys: list):
        config = {}
        for key in keys:
            config[key] = self.get(key)
        return config

    @staticmethod
    def __check_config_integrity(config):
        config_keys = ['toggl_user', 'toggl_workspace_id', 'toggl_start_date',
                       'toggl_end_date', 'toggl_api_token']
        for key in config_keys:
            if key not in config:
                raise ConfigException(
                    "There's a key missing in the configuration")
