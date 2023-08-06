import click
import os

BASE_PATH = click.get_app_dir('nalej-platformer', force_posix=True)
CONFIG_PATH = os.path.join(BASE_PATH, "config.yaml")
SP_PATH = os.path.join(BASE_PATH, ".azure-sp.json")
KC_PATH = os.path.join(BASE_PATH, "kubeconfigs")
