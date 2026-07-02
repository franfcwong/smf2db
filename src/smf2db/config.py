"""This module provides the Smf2db config functionality."""
# smf2db/config.py

import os
from pathlib import Path
from typing import Union

import click
import yaml

from smf2db import (
    ERRORS, FILE_ERROR
)


class ConfigManager:
    def __init__(self, config_path: os.PathLike):
        self.config_file_path = Path(config_path)
        self.config = {}

    def load_config(self) -> Union[dict, tuple]:
        """Load configuration for a specific environment"""
        try:
            with open(self.config_file_path, 'r') as file:
                self.config = yaml.safe_load(file)
            # print(f"✓ Loaded configuration for {self.config_file_name}")
            return self.config
        except FileNotFoundError:
            # print(f"✗ Configuration file not found: {config_file}")
            return ERRORS[FILE_ERROR], f"✗ Configuration file not found: {click.format_filename(self.config_file_path)}"
        except yaml.YAMLError as e:
            # print(f"✗ Error parsing YAML: {e}")
            return ERRORS[FILE_ERROR], f"✗ Error parsing YAML: {e}"

    def get(self, key_path, default=None):
        """Get a configuration value using dot notation"""
        keys = key_path.split('.')
        value = self.config

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def save_config(self, config_data):
        """Save configuration to a file"""
        config_dir = os.path.split(self.config_file_path)[0]
        try:
            os.makedirs(config_dir, exist_ok=True)
        except OSError as e:
            raise click.ClickException(f"✗ Creation of configuration directory failed:{str(e)}")

        with open(self.config_file_path, 'w') as file:
            yaml.dump(config_data, file, default_flow_style=False)

        click.echo(f"✓ Saved configuration for {click.format_filename(self.config_file_path)}")

