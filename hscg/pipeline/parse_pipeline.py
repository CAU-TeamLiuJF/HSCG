import os
from ..base import CustomConfig, str_to_hump
from .. import core as cores


pipeline = [
    'data',
    'short_reads_treatment',
    'long_reads_treatment',
    'assembly',
    'scaffolding',
    'scaffolding_ref_based',
    'gap_filling'
]


def generate_custom_config():
    custom_config = CustomConfig()
    for item in pipeline:
        module = getattr(cores, str_to_hump(item))([], [], [])
        for item in module.get_pipeline_config():
            section, param, value = item
            custom_config.set_pipeline_value(section, param, str(value))

        for item in module.get_binary_config():
            section, param, value = item
            custom_config.set_binary_value(section, param, str(value))

        for item in module.get_core_config():
            section, param, value = item
            custom_config.set_core_value(section, param, str(value))

    custom_config.output_pipeline_value()
    custom_config.output_binary_value()
    custom_config.output_core_value()


def read_and_run_custom_config():
    custom_config = CustomConfig()
    pipeline_config = custom_config.parse_pipeline_config()
    binary_config = custom_config.parse_binary_config()
    core_config = custom_config.parse_core_config()

    for item in pipeline:
        module = getattr(cores, str_to_hump(item))(pipeline_config, binary_config, core_config)
        module.run_pipeline()
        
