import logging
import os
from datetime import datetime
from enum import Enum
from typing import Optional
from rich.console import Console
from rich.logging import RichHandler

class LogLevel(Enum):
    """Log levels for ConSolar framework"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class ConSolarLogger:
    """Enhanced logging system for ConSolar framework"""
    
    def __init__(self, name: str = "ConSolar", log_level: LogLevel = LogLevel.INFO, 
                 log_dir: str = "logs", log_filename: str = "consolar.log"):
        self.console = Console()
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.value))
        self.log_dir = log_dir
        self.log_filename = log_filename
        
        # Prevent duplicate handlers
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup console and file handlers"""
        # Rich console handler for beautiful output
        console_handler = RichHandler(console=self.console, rich_tracebacks=True)
        console_handler.setFormatter(logging.Formatter(
            fmt="%(message)s",
            datefmt="[%X]"
        ))
        
        # File handler for persistent logging - use custom directory and filename
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        log_file_path = os.path.join(self.log_dir, self.log_filename)
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setFormatter(logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        ))
        
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def debug(self, message: str, **kwargs) -> None:
        """Log debug message"""
        self.logger.debug(message, **kwargs)
    
    def info(self, message: str, **kwargs) -> None:
        """Log info message"""
        self.logger.info(message, **kwargs)
    
    def warning(self, message: str, **kwargs) -> None:
        """Log warning message"""
        self.logger.warning(message, **kwargs)
    
    def error(self, message: str, **kwargs) -> None:
        """Log error message"""
        self.logger.error(message, **kwargs)
    
    def critical(self, message: str, **kwargs) -> None:
        """Log critical message"""
        self.logger.critical(message, **kwargs)
    
    def log_exception(self, message: str = "An exception occurred") -> None:
        """Log exception with traceback"""
        self.logger.exception(message)
    
    def set_level(self, level: LogLevel) -> None:
        """Change logging level"""
        self.logger.setLevel(getattr(logging, level.value))
    
    def log_plugin_action(self, plugin_name: str, action: str, status: str = "SUCCESS") -> None:
        """Specialized logging for plugin actions"""
        self.info(f"[bold cyan]Plugin[/bold cyan] {plugin_name}: {action} - [green]{status}[/green]")
    
    def log_user_action(self, action: str, details: Optional[str] = None) -> None:
        """Log user interactions"""
        msg = f"[bold blue]User Action:[/bold blue] {action}"
        if details:
            msg += f" - {details}"
        self.info(msg)

# Legacy support - keep the old function but mark as deprecated
def log(target, show_target, repeat: int = 1) -> None:
    """Legacy log function - DEPRECATED. Use ConSolarLogger instead."""
    logger = ConSolarLogger()
    logger.warning("Using deprecated log function. Please use ConSolarLogger instead.")
    
    if show_target:
        for i in range(repeat):
            logger.info(str(target))
    else:
        logger.warning("Logging is disabled because 'show_target' is set to False.")

# Global logger instance
logger = ConSolarLogger()
