"""
ConSolar Framework - A Console Framework for Interactive Applications
"""

from .core import user, __version__, __framework__
from .plugin_manger import Plugin, PluginManager, EnhancedPlugin, plugin_manager
from .logger import ConSolarLogger
from .config_manager import ConfigManager, config_manager
from .error_handler import ConSolarError, PluginError, safe_execute

# Framework class (compatibility with README documentation)
class Framework:
    def __init__(self):
        self.plugin_manager = PluginManager()
        self.plugins = self.plugin_manager.plugins
    
    def register_plugin(self, plugin: Plugin):
        """Registers a plugin instance"""
        plugin.register(self.plugin_manager)
        self.plugin_manager.plugins.append(plugin)

# Function to load plugins dynamically (compatibility with README documentation)
def load_plugin(module_name: str, class_name: str) -> Plugin:
    """Dynamically loads a plugin class from a module"""
    import importlib
    module = importlib.import_module(module_name)
    plugin_class = getattr(module, class_name)
    return plugin_class()

__all__ = [
    'user', 'Framework', 'Plugin', 'load_plugin', 'PluginManager', 
    'EnhancedPlugin', 'ConSolarLogger', 'ConfigManager', 'ConSolarError',
    'PluginError', 'safe_execute', 'plugin_manager', 'config_manager',
    '__version__', '__framework__', 'parse', 'user.user_value'
]
