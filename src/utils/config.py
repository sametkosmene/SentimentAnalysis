# src/utils/config.py

import yaml
import os

class Config:
    def __init__(self, config_file):
        self.config = self.load_config(config_file)

    def load_config(self, config_file):
        """
        Load a YAML configuration file.
        :param config_file: Path to the YAML configuration file.
        :return: Dictionary containing the configuration.
        """
        with open(config_file, 'r') as file:
            return yaml.safe_load(file)

    def get(self, key, default=None):
        """
        Get a configuration value by key.
        :param key: The key to look up in the configuration.
        :param default: The default value if the key is not found.
        :return: The value from the configuration or the default value.
        """
        return self.config.get(key, default)

# Example usage
if __name__ == "__main__":
    # Load configuration from a file
    app_config = Config('config/app_config.yml')
    
    # Access specific configuration values
    kafka_topic = app_config.get('kafka_topic')
    print(f"Kafka Topic: {kafka_topic}")
