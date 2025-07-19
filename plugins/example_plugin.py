"""
Example Plugin for ConSolar Framework
This demonstrates how to create a plugin using the EnhancedPlugin base class.
"""

__version__ = "1.0.0"
__dependencies__ = []  # No dependencies for this example

from ConSolar.plugin_manger import EnhancedPlugin
from ConSolar.logger import ConSolarLogger

class ExamplePlugin(EnhancedPlugin):
    """
    A simple example plugin that demonstrates plugin capabilities.
    """
    
    def __init__(self):
        super().__init__()
        self.logger = ConSolarLogger(f"Plugin-{self.name}")
    
    def on_register(self, framework):
        """Called when plugin is registered"""
        self.logger.info("Example plugin registered successfully!")
        # Add plugin commands or functionality here
        
    def on_unregister(self):
        """Called when plugin is unregistered"""
        self.logger.info("Example plugin unregistered")
    
    def do_something(self):
        """Example plugin functionality"""
        self.logger.info("Example plugin is doing something!")
        return "Hello from Example Plugin!"
    
    def get_status(self):
        """Get plugin status"""
        return {
            "name": self.name,
            "version": self.version,
            "enabled": self.is_enabled(),
            "description": self.description
        }
