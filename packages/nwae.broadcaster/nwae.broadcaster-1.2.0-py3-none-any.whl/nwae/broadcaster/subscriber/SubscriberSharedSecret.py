#-*- coding: utf-8 -*-

from nwae.utils.BaseConfig import BaseConfig
from nwae.utils.Log import Log
from inspect import getframeinfo, currentframe


class SubscriberSharedSecret(BaseConfig):

    singleton_config = None
    # Initialize this from somewhere first
    singleton_config_file_path = None

    @staticmethod
    def init_singleton_config():
        if SubscriberSharedSecret.singleton_config is None:
            Log.important(
                str(__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Initializing secret config for the first time using file "'
                + str(SubscriberSharedSecret.singleton_config_file_path) + '"..'
            )
            SubscriberSharedSecret.singleton_config = SubscriberSharedSecret(
                config_file = SubscriberSharedSecret.singleton_config_file_path
            )
        return SubscriberSharedSecret.singleton_config

    def __init__(
            self,
            config_file,
            ignore_non_existant_config_file=True
    ):
        try:
            super().__init__(
                config_file = config_file,
                ignore_non_existant_config_file = ignore_non_existant_config_file
            )
        except Exception as ex:
            errmsg = \
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno) \
                + ': Error calling base config for config file "' + str(config_file) \
                + '". Exception ' + str(ex) + '.'
            Log.error(errmsg)
            # Ignore error, just use default values

        self.config_file = config_file
        self.reload_config()
        return

    def reload_config(
            self
    ):
        # Call base class first
        Log.debug(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno) \
            + ': Calling base class reload config for "' + str(self.config_file) + '"..'
        )
        super().reload_config()

        try:
            self.reset_default_config()
        except Exception as ex:
            errmsg = str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno) \
                     + ': Error initializing config file "' + str(self.config_file) \
                     + '". Exception message ' + str(ex)
            Log.critical(errmsg)
            raise Exception(errmsg)

        return

    #
    # For those params not found in config file, we give default values
    #
    def reset_default_config(
            self
    ):
        param_values_to_set = {}

        for param in param_values_to_set.keys():
            default_value = param_values_to_set[param]
            self.set_default_value_if_not_exist(
                param=param,
                default_value=default_value
            )
        return


if __name__ == '__main__':
    import time

    SubscriberSharedSecret.singleton_config_file_path = '/usr/local/git/nwae/nwae.broadcaster/app.data/secret/secret.staging.cf'

    config = SubscriberSharedSecret.init_singleton_config()
    print(config.param_value)
    print(config.get_config(param='anyone'))
    print(config.get_config(param='nosuchid'))
