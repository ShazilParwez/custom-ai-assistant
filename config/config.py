import os
import yaml
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class AppConfig:
    """
    Application configuration loader.

    Loads settings from config.yaml and overrides sensitive values
    (like API keys) using environment variables.
    """

    def __init__(self):
        self.config = self.load_config()

    def load_config(self):
        # Build absolute path to config.yaml
        config_path = os.path.join(os.path.dirname(__file__), "config.yaml")

        with open(config_path, "r") as file:
            config = yaml.safe_load(file)

        # Replace API key with environment variable if present
        if "api" in config and "key" in config["api"]:
            config["api"]["key"] = os.getenv("GROQ_API_KEY")

        return config


# Initialize configuration
app_config = AppConfig()

# Store loaded configuration
config = app_config.config

# Extract API key
API_KEY = config["api"]["key"]