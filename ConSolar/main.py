#!/usr/bin/env python3
"""
ConSolar Framework - Main Entry Point
"""

import sys
from .core import *
from .plugin_manger import plugin_manager
from .logger import ConSolarLogger
from .config_manager import config_manager

logger = ConSolarLogger("ConSolar")

def main():
    """Main entry point for ConSolar framework"""
    logger.info("ConSolar Framework starting...")
    
    # Initialize the framework
    print("🌟 Welcome to ConSolar")
    print("A Console Framework for Interactive Applications")
    print("-" * 50)
    
    # Load plugins
    try:
        plugin_manager.load_all_plugins()
        print(f"✅ Loaded {len(plugin_manager.plugins)} plugins")
    except Exception as e:
        logger.error(f"Error loading plugins: {e}")
    
    # Basic interactive menu
    while True:
        try:
            print("\n🚀 ConSolar Framework")
            print("1. List loaded plugins")
            print("2. Test user input")
            print("3. Test multi-choice")
            print("4. Exit")
            
            choice = input("Select option (1-4): ").strip()
            
            if choice == "1":
                plugins = plugin_manager.list_plugins()
                if plugins:
                    print(f"\n📦 Loaded plugins ({len(plugins)}):")
                    for i, plugin in enumerate(plugins, 1):
                        print(f"  {i}. {plugin}")
                else:
                    print("\n❌ No plugins loaded")
                    
            elif choice == "2":
                user.user_input("Enter some text")
                print(f"You entered: {user.user_value}")
                
            elif choice == "3":
                options = ["Option 1", "Option 2", "Option 3", "Exit"]
                user.multi_choice("Select an option", options)
                print(f"You selected: {user.user_value}")
                
            elif choice == "4":
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please select 1-4.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted by user. Goodbye!")
            break
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
