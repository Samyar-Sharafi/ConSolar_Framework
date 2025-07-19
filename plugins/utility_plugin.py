"""
Utility Plugin for ConSolar Framework
Provides utility functions and tools.
"""

__version__ = "2.1.0"
__dependencies__ = []

from ConSolar.plugin_manger import EnhancedPlugin
from ConSolar.logger import ConSolarLogger
import hashlib
import time

class UtilityPlugin(EnhancedPlugin):
    """
    A utility plugin that provides common utility functions.
    """
    
    def __init__(self):
        super().__init__()
        self.logger = ConSolarLogger(f"Plugin-{self.name}")
        self.start_time = time.time()
    
    def on_register(self, framework):
        """Called when plugin is registered"""
        self.logger.info("Utility plugin loaded with useful tools!")
        
    def on_unregister(self):
        """Called when plugin is unregistered"""
        uptime = time.time() - self.start_time
        self.logger.info(f"Utility plugin ran for {uptime:.2f} seconds")
    
    def hash_text(self, text: str, algorithm: str = "sha256") -> str:
        """Generate hash of text"""
        if algorithm == "md5":
            return hashlib.md5(text.encode()).hexdigest()
        elif algorithm == "sha256":
            return hashlib.sha256(text.encode()).hexdigest()
        else:
            raise ValueError("Unsupported hash algorithm")
    
    def get_timestamp(self) -> str:
        """Get current timestamp"""
        return time.strftime("%Y-%m-%d %H:%M:%S")
    
    def measure_time(self):
        """Get plugin uptime"""
        return time.time() - self.start_time
