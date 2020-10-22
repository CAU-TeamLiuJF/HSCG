import configparser
import os

class BaseConfigParam:
    """ Base Class of Configuration Parameters """
    def __init__(self):
        pass

    def list_all_member(self):
        """ [(section, param, value)] """
        item_list = []
        for name, value in vars(self).items():
            if name != "section":
                item_list.append((self.section, name, value))
        return item_list


class CustomConfig(object):
    """ Configuration class """
    def __init__(self):
        super().__init__()
        self.pipeline_config = configparser.ConfigParser()
        self.pipeline_file = 'opt.ini'

        self.binary_config = configparser.ConfigParser()
        self.binary_file = 'bopt.ini'

        self.core_config = configparser.ConfigParser()
        self.core_file = 'parameter.ini'

    """
    Set and get section, options, value
    """
    def set_section_param_value(self, config_object, section, param, value):
        try:
            if section not in config_object.sections():
                config_object.add_section(section)
            config_object.set(section, param, value)
        except configparser.DuplicateSectionError:
            print("Section/Param repeats.")

    def get_section_param_value(self, config_object, section, param):
        return config_object.get(section, param)

    def set_pipeline_value(self, section, param, value):
        self.set_section_param_value(self.pipeline_config, section, param, value)

    def set_binary_value(self, section, param, value):
        self.set_section_param_value(self.binary_config, section, param, value)

    def set_core_value(self, section, param, value):
        self.set_section_param_value(self.core_config, section, param, value)

    """
    Output configuration file
    """
    def output_config(self, config_object, filename):
        with open(filename, 'w') as f:
            config_object.write(f)

    def output_pipeline_value(self):
        self.output_config(self.pipeline_config, self.pipeline_file)

    def output_binary_value(self):
        self.output_config(self.binary_config, self.binary_file)

    def output_core_value(self):
        self.output_config(self.core_config, self.core_file)

    """
    Read and parse configuration file
    """
    def parse_pipeline_config(self):
        if not os.path.exists(self.pipeline_file):
            raise ValueError('No {} in current path.'.format(self.pipeline_file))
        self.pipeline_config.read(self.pipeline_file)
        config_params = {}
        for section in self.pipeline_config.sections():
            config_params[section] = {}
            for option in self.pipeline_config.options(section):
                config_params[section][option] = self.pipeline_config.get(section, option)
        return config_params

    def parse_binary_config(self):
        if not os.path.exists(self.binary_file):
            raise ValueError('No {} in current path.'.format(self.binary_file))
        self.binary_config.read(self.binary_file)
        config_params = {}
        for section in self.binary_config.sections():
            config_params[section] = {}
            for option in self.binary_config.options(section):
                config_params[section][option] = self.binary_config.get(section, option)
        return config_params


    def parse_core_config(self):
        if not os.path.exists(self.core_file):
            raise ValueError('No {} in current path.'.format(self.core_file))
        self.core_config.read(self.core_file)
        config_params = {}
        for section in self.core_config.sections():
            config_params[section] = {}
            for option in self.core_config.options(section):
                config_params[section][option] = self.core_config.get(section, option)
        return config_params
