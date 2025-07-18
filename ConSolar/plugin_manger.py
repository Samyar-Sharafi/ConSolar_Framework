
import importlib

#---Plugin management---#
class Framework:
    def __init__(self):
        self.plugins = []

    def register_plugin(self, plugin):
        try:
            self.plugins.append(plugin)
            plugin.register(self)
        except Exception as e:
            print(f"Error registering plugin {plugin}: {e}")

class Plugin:
    def run(self):
        pass  # Plugins must implement this method

def load_plugin(module_name, class_name):
    module = importlib.import_module(module_name)
    plugin_class = getattr(module, class_name)
    return plugin_class()

def unload_plugin(plugin):
    try:
        plugin.unregister()
    except Exception as e:
        print(f"Error unloading plugin {plugin}: {e}")
#---Plugin management---#
