from nalej_platformer.utils import print_debug
from nalej_platformer.config import Configuration


def load_configuration(ctx):
    config_path = ctx.obj['CONFIG_PATH']
    resources_path = ctx.obj['RESOURCES_PATH']
    print_debug(f'Using config file: {config_path}')

    config = Configuration.load_from_file(config_path, resources_path)

    config.find_missing_binaries()
    config.validate()

    ctx.obj['CONFIGURATION'] = config
