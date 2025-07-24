import sys
import signal
import functools
from typing import Optional, Callable, Any
from rich.console import Console
from rich.traceback import install
from rich.panel import Panel
from logger import ConSolarLogger, LogLevel

# Initialize console and logger
console = Console()
logger = ConSolarLogger("ErrorHandler")
install(show_locals=True)  # Rich traceback with local variables

# Custom Exception Classes
class ConSolarError(Exception):
    """Base exception for ConSolar framework"""
    def __init__(self, message: str, exit_code: int = 1):
        self.message = message
        self.exit_code = exit_code
        super().__init__(self.message)

class PluginError(ConSolarError):
    """Exception for plugin-related errors"""
    def __init__(self, plugin_name: str, message: str):
        self.plugin_name = plugin_name
        super().__init__(f"Plugin '{plugin_name}': {message}", exit_code=2)

class ConfigurationError(ConSolarError):
    """Exception for configuration-related errors"""
    def __init__(self, config_file: str, message: str):
        self.config_file = config_file
        super().__init__(f"Configuration '{config_file}': {message}", exit_code=3)

class ValidationError(ConSolarError):
    """Exception for input validation errors"""
    def __init__(self, field: str, value: Any, message: str):
        self.field = field
        self.value = value
        super().__init__(f"Validation error for '{field}' ({value}): {message}", exit_code=4)

# Error Handler Functions
def handle_keyboard_interrupt(signum, frame):
    """Handle Ctrl+C gracefully"""
    console.print("\n[yellow]⚠️  Operation cancelled by user[/yellow]")
    logger.info("User interrupted the operation with Ctrl+C")
    sys.exit(0)

def handle_general_exception(exc_type, exc_value, exc_traceback):
    """Handle all uncaught exceptions"""
    if issubclass(exc_type, KeyboardInterrupt):
        handle_keyboard_interrupt(None, None)
    elif issubclass(exc_type, ConSolarError):
        # Handle ConSolar specific errors
        error_panel = Panel(
            f"[bold red]Error:[/bold red] {exc_value.message}",
            title="ConSolar Framework Error",
            border_style="red"
        )
        console.print(error_panel)
        logger.error(f"ConSolar Error: {exc_value.message}")
        sys.exit(exc_value.exit_code)
    else:
        # Handle unexpected errors with rich traceback
        console.print("\n[bold red]An unexpected error occurred:[/bold red]")
        console.print_exception()
        logger.critical("Unexpected error occurred", exc_info=True)
        sys.exit(1)

# Decorator for safe function execution
def safe_execute(show_traceback: bool = False):
    """Decorator to safely execute functions with error handling"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except KeyboardInterrupt:
                handle_keyboard_interrupt(None, None)
            except ConSolarError as e:
                console.print(f"[bold red]Error:[/bold red] {e.message}")
                logger.error(f"Function '{func.__name__}' failed: {e.message}")
                if show_traceback:
                    console.print_exception()
                return None
            except Exception as e:
                console.print(f"[bold red]Unexpected error in {func.__name__}:[/bold red] {str(e)}")
                logger.exception(f"Unexpected error in function '{func.__name__}'")
                if show_traceback:
                    console.print_exception()
                return None
        return wrapper
    return decorator

# Context manager for safe operations
class SafeOperation:
    """Context manager for safe operations with automatic error handling"""
    
    def __init__(self, operation_name: str, show_errors: bool = True):
        self.operation_name = operation_name
        self.show_errors = show_errors
        
    def __enter__(self):
        logger.debug(f"Starting operation: {self.operation_name}")
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            logger.debug(f"Operation completed successfully: {self.operation_name}")
            return True
        
        if issubclass(exc_type, KeyboardInterrupt):
            handle_keyboard_interrupt(None, None)
        elif issubclass(exc_type, ConSolarError):
            if self.show_errors:
                console.print(f"[bold red]Error in {self.operation_name}:[/bold red] {exc_value.message}")
            logger.error(f"Operation '{self.operation_name}' failed: {exc_value.message}")
            return True  # Suppress the exception
        else:
            if self.show_errors:
                console.print(f"[bold red]Unexpected error in {self.operation_name}:[/bold red] {str(exc_value)}")
            logger.exception(f"Unexpected error in operation '{self.operation_name}'")
            return True  # Suppress the exception

# Validation helpers
def validate_not_empty(value: str, field_name: str) -> str:
    """Validate that a string is not empty"""
    if not value or not value.strip():
        raise ValidationError(field_name, value, "Cannot be empty")
    return value.strip()

def validate_file_exists(file_path: str, field_name: str) -> str:
    """Validate that a file exists"""
    from pathlib import Path
    if not Path(file_path).exists():
        raise ValidationError(field_name, file_path, "File does not exist")
    return file_path

def validate_positive_int(value: int, field_name: str) -> int:
    """Validate that an integer is positive"""
    if value <= 0:
        raise ValidationError(field_name, value, "Must be a positive integer")
    return value

# Initialize error handling
def initialize_error_handling():
    """Initialize the error handling system"""
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, handle_keyboard_interrupt)  # Ctrl+C
    if hasattr(signal, 'SIGTERM'):
        signal.signal(signal.SIGTERM, handle_keyboard_interrupt)  # Termination
    
    # Set up global exception handler
    sys.excepthook = handle_general_exception
    
    logger.debug("Error handling system initialized")

# Auto-initialize when module is imported
initialize_error_handling()
