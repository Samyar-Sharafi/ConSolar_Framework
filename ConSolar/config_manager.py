import os
import json
from typing import Dict, Any, Optional
from pathlib import Path
from .logger import ConSolarLogger
from .error_handler import ConfigurationError, safe_execute

logger = ConSolarLogger("ConfigManager")

class ConfigManager:
    """JSON-based configuration management for ConSolar framework"""
    
    def __init__(self, config_file: str = "config.json", config_dir: str = "config"):
        self.config_file = config_file
        self.config_dir = config_dir
        self.config_path = os.path.join(config_dir, config_file)
        self.config_data: Dict[str, Any] = {}
        self.defaults: Dict[str, Any] = {}
        
        # Ensure config directory exists
        os.makedirs(config_dir, exist_ok=True)
        logger.debug(f"ConfigManager initialized with file: {self.config_path}")
    
    def set_defaults(self, defaults: Dict[str, Any]) -> None:
        """Set default configuration values"""
        self.defaults = defaults
        logger.debug(f"Default configuration set with {len(defaults)} keys")
    
    @safe_execute(show_traceback=True)
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config_data = json.load(f)
                logger.info(f"Configuration loaded from {self.config_path}")
            else:
                logger.warning(f"Config file not found: {self.config_path}, using defaults")
                self.config_data = self.defaults.copy()
                self.save_config()  # Create the file with defaults
                
        except json.JSONDecodeError as e:
            raise ConfigurationError(self.config_file, f"Invalid JSON format: {str(e)}")
        except Exception as e:
            raise ConfigurationError(self.config_file, f"Failed to load config: {str(e)}")
        
        # Merge with defaults for missing keys
        for key, value in self.defaults.items():
            if key not in self.config_data:
                self.config_data[key] = value
        
        return self.config_data
    
    @safe_execute(show_traceback=True)
    def save_config(self) -> None:
        """Save current configuration to JSON file"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=4, ensure_ascii=False)
            logger.info(f"Configuration saved to {self.config_path}")
        except Exception as e:
            raise ConfigurationError(self.config_file, f"Failed to save config: {str(e)}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key"""
        value = self.config_data.get(key, default)
        logger.debug(f"Config get '{key}': {value}")
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value and save"""
        self.config_data[key] = value
        logger.debug(f"Config set '{key}': {value}")
        self.save_config()
    
    def get_nested(self, key_path: str, default: Any = None, separator: str = ".") -> Any:
        """Get nested configuration value using dot notation (e.g., 'database.host')"""
        keys = key_path.split(separator)
        value = self.config_data
        
        try:
            for key in keys:
                value = value[key]
            logger.debug(f"Config get nested '{key_path}': {value}")
            return value
        except (KeyError, TypeError):
            logger.debug(f"Config nested key '{key_path}' not found, using default: {default}")
            return default
    
    def set_nested(self, key_path: str, value: Any, separator: str = ".") -> None:
        """Set nested configuration value using dot notation"""
        keys = key_path.split(separator)
        config = self.config_data
        
        # Navigate to the parent of the target key
        for key in keys[:-1]:
            if key not in config or not isinstance(config[key], dict):
                config[key] = {}
            config = config[key]
        
        # Set the final value
        config[keys[-1]] = value
        logger.debug(f"Config set nested '{key_path}': {value}")
        self.save_config()
    
    def update(self, new_config: Dict[str, Any]) -> None:
        """Update configuration with new values"""
        self.config_data.update(new_config)
        logger.info(f"Configuration updated with {len(new_config)} new values")
        self.save_config()
    
    def reset_to_defaults(self) -> None:
        """Reset configuration to default values"""
        self.config_data = self.defaults.copy()
        logger.info("Configuration reset to defaults")
        self.save_config()
    
    def has_key(self, key: str) -> bool:
        """Check if configuration has a specific key"""
        return key in self.config_data
    
    def remove_key(self, key: str) -> None:
        """Remove a key from configuration"""
        if key in self.config_data:
            del self.config_data[key]
            logger.debug(f"Config key '{key}' removed")
            self.save_config()
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration data"""
        return self.config_data.copy()
    
    def export_config(self, export_path: str) -> None:
        """Export configuration to another JSON file"""
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=4, ensure_ascii=False)
            logger.info(f"Configuration exported to {export_path}")
        except Exception as e:
            raise ConfigurationError(export_path, f"Failed to export config: {str(e)}")
    
    def import_config(self, import_path: str, merge: bool = True) -> None:
        """Import configuration from another JSON file"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)
            
            if merge:
                self.config_data.update(imported_config)
                logger.info(f"Configuration merged from {import_path}")
            else:
                self.config_data = imported_config
                logger.info(f"Configuration replaced from {import_path}")
            
            self.save_config()
        except Exception as e:
            raise ConfigurationError(import_path, f"Failed to import config: {str(e)}")

# Environment Variable Helper
class EnvConfig:
    """Helper class for environment variable configuration"""
    
    @staticmethod
    def get_env(key: str, default: Any = None) -> str:
        """Get environment variable value"""
        value = os.getenv(key, default)
        logger.debug(f"Environment variable '{key}': {value}")
        return value
    
    @staticmethod
    def get_env_bool(key: str, default: bool = False) -> bool:
        """Get environment variable as boolean"""
        value = os.getenv(key, str(default)).lower()
        return value in ('true', '1', 'yes', 'on')
    
    @staticmethod
    def get_env_int(key: str, default: int = 0) -> int:
        """Get environment variable as integer"""
        try:
            return int(os.getenv(key, str(default)))
        except ValueError:
            logger.warning(f"Invalid integer value for env var '{key}', using default: {default}")
            return default
    
    @staticmethod
    def get_env_list(key: str, separator: str = ",", default: list = None) -> list:
        """Get environment variable as list (comma-separated by default)"""
        if default is None:
            default = []
        
        value = os.getenv(key)
        if value:
            return [item.strip() for item in value.split(separator)]
        return default

# Global configuration instance
config_manager = ConfigManager()

# Set some default configuration
default_config = {
    "framework": {
        "name": "ConSolar",
        "version": "0.0.1b",
        "debug": False
    },
    "logging": {
        "level": "INFO",
        "log_dir": "logs",
        "log_file": "consolar.log"
    },
    "plugins": {
        "plugin_dir": "plugins",
        "auto_load": True
    },
    "ui": {
        "theme": "default",
        "show_progress": True
    }
}

config_manager.set_defaults(default_config)
