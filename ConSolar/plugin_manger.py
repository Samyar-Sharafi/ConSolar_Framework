
import importlib
import os
import sys
from typing import List, Type
from .error_handler import safe_execute, PluginError
from .logger import ConSolarLogger

logger = ConSolarLogger("PluginManager")

# Plugin Base Class
class Plugin:
    def register(self, framework):
        raise NotImplementedError("Plugins must implement the 'register' method")

# Plugin Manager
class PluginManager:
    def __init__(self, plugin_dir: str = "plugins"):
        self.plugin_dir = plugin_dir
        self.plugins: List[Plugin] = []
        self.discovered_modules: List[str] = []
        logger.debug(f"PluginManager initialized with directory: {self.plugin_dir}")

    def discover_plugins(self) -> None:
        """Automatically discover plugin modules in the specified directory"""
        logger.info(f"Discovering plugins in: {self.plugin_dir}")
        if not os.path.exists(self.plugin_dir):
            logger.warning(f"Plugin directory does not exist: {self.plugin_dir}")
            return

        for file in os.listdir(self.plugin_dir):
            if file.endswith(".py") and not file.startswith("__"):
                module_name = file[:-3]  # Strip .py extension
                self.discovered_modules.append(module_name)

    @safe_execute(show_traceback=True)
    def load_discovered_plugins(self) -> None:
        """Load all discovered plugin modules"""
        for module_name in self.discovered_modules:
            logger.info(f"Loading plugin module: {module_name}")
            try:
                module_path = f"{self.plugin_dir}.{module_name}"
                module = importlib.import_module(module_path)
                self._register_plugin(module)
            except Exception as e:
                logger.error(f"Failed to load plugin '{module_name}': {e}")

    def _register_plugin(self, module) -> None:
        """Register a plugin module"""
        try:
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, Plugin) and attr is not Plugin:
                    plugin_instance = attr()
                    plugin_instance.register(self)
                    self.plugins.append(plugin_instance)
                    logger.info(f"Registered plugin: {attr_name}")
        except Exception as e:
            raise PluginError(attr_name, str(e)) from e

    def unload_plugin(self, plugin: Plugin) -> None:
        """Unload a plugin"""
        try:
            plugin.unregister()
            self.plugins.remove(plugin)
            logger.info(f"Unloaded plugin: {plugin.__class__.__name__}")
        except Exception as e:
            logger.error(f"Error unloading plugin {plugin}: {e}")

    def get_plugin_by_name(self, name: str) -> Plugin:
        """Get a plugin by its class name"""
        for plugin in self.plugins:
            if plugin.__class__.__name__ == name:
                return plugin
        raise PluginError(name, "Plugin not found")

    def list_plugins(self) -> List[str]:
        """List all loaded plugin names"""
        return [plugin.__class__.__name__ for plugin in self.plugins]

    def load_all_plugins(self) -> None:
        """Discover and load all plugins in one call"""
        self.discover_plugins()
        self.load_discovered_plugins()
        logger.info(f"Loaded {len(self.plugins)} plugins total")

    def unload_all_plugins(self) -> None:
        """Unload all plugins"""
        for plugin in self.plugins.copy():  # Copy to avoid modification during iteration
            self.unload_plugin(plugin)
        logger.info("All plugins unloaded")

    def reload_plugin(self, plugin_name: str) -> None:
        """Reload a specific plugin"""
        # Find and unload the plugin
        plugin = self.get_plugin_by_name(plugin_name)
        module_name = plugin.__module__
        self.unload_plugin(plugin)
        
        # Reload the module
        import importlib
        if module_name in sys.modules:
            importlib.reload(sys.modules[module_name])
        
        # Re-register the plugin
        module = importlib.import_module(module_name)
        self._register_plugin(module)
        logger.info(f"Reloaded plugin: {plugin_name}")

# Plugin Discovery Utilities
class PluginInfo:
    """Information about a discovered plugin"""
    def __init__(self, name: str, path: str, version: str = "unknown", description: str = ""):
        self.name = name
        self.path = path
        self.version = version
        self.description = description

def scan_for_plugins(directory: str) -> List[PluginInfo]:
    """Scan directory for plugin information"""
    plugins = []
    if not os.path.exists(directory):
        logger.warning(f"Plugin directory does not exist: {directory}")
        return plugins
    
    for file in os.listdir(directory):
        if file.endswith(".py") and not file.startswith("__"):
            file_path = os.path.join(directory, file)
            plugin_name = file[:-3]
            
            # Try to extract plugin information from the file
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    # Look for version and description in docstrings or comments
                    version = "unknown"
                    description = ""
                    
                    # Simple extraction (could be improved with AST parsing)
                    if '__version__' in content:
                        import re
                        version_match = re.search(r"""__version__\s*=\s*["\']([^"\']*)["\'']""", content)
                        if version_match:
                            version = version_match.group(1)
                    
                    plugins.append(PluginInfo(plugin_name, file_path, version, description))
            except Exception as e:
                logger.warning(f"Could not read plugin info from {file}: {e}")
                plugins.append(PluginInfo(plugin_name, file_path))
    
    return plugins

# Enhanced Plugin Base Class
class EnhancedPlugin(Plugin):
    """Enhanced plugin base class with more features"""
    
    def __init__(self):
        self.name = self.__class__.__name__
        self.version = getattr(self, '__version__', '1.0.0')
        self.description = getattr(self, '__doc__', 'No description available')
        self.enabled = True
        self.dependencies = getattr(self, '__dependencies__', [])
    
    def register(self, framework):
        """Register the plugin with the framework"""
        logger.info(f"Registering plugin: {self.name} v{self.version}")
        # Check dependencies
        self._check_dependencies(framework)
        # Custom registration logic can be overridden
        self.on_register(framework)
    
    def unregister(self):
        """Unregister the plugin"""
        logger.info(f"Unregistering plugin: {self.name}")
        self.on_unregister()
    
    def on_register(self, framework):
        """Override this method for custom registration logic"""
        pass
    
    def on_unregister(self):
        """Override this method for custom cleanup logic"""
        pass
    
    def _check_dependencies(self, framework):
        """Check if plugin dependencies are met"""
        for dep in self.dependencies:
            if dep not in framework.list_plugins():
                raise PluginError(self.name, f"Missing dependency: {dep}")
    
    def enable(self):
        """Enable the plugin"""
        self.enabled = True
        logger.info(f"Enabled plugin: {self.name}")
    
    def disable(self):
        """Disable the plugin"""
        self.enabled = False
        logger.info(f"Disabled plugin: {self.name}")
    
    def is_enabled(self) -> bool:
        """Check if plugin is enabled"""
        return self.enabled

# Global plugin manager instance
plugin_manager = PluginManager()

#---Plugin management---#
