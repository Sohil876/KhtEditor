import sys
import os
import glob
import khteditor
#from PyQt4.QtCore import QSettings

PATHS = [os.path.join(khteditor.__path__[0],'plugins'),os.path.join(os.path.expanduser("~"),'.khteditor','plugins')]

class Plugin(object):
    capabilities = []

    def __repr__(self):
        return '<%s %r>' % (
            self.__class__.__name__,
            self.capabilities
        )

def filter_plugins_by_capability(capability,plugins_list):
    result = []
    for plugin in plugins_list:
        if capability in plugin.capabilities:
            result.append(plugin)
    return result
            
def get_plugins_by_capability(capability):
    result = []
    for plugin in Plugin.__subclasses__():
        if capability in plugin.capabilities:
            result.append(plugin)
    return result

def load_plugins(plugins):
    for plugin in plugins:
        __import__(plugin, None, None, [''])

def discover_plugin_in_paths():
    plugins = []
    for path in PATHS:
        for plug_path in glob.glob(os.path.join(path,'*.pyc')):
            plugin_name = os.path.splitext(os.path.basename(plug_path))[0] 
            if not (plugin_name in plugins):
                print 'Discover plugin : ' + plugin_name
                plugins.append(plugin_name)
    return plugins
    
def init_plugin_system():
    #Add path to sys.path
    for path in PATHS:
        if not path in sys.path:
            sys.path.insert(0, path)
            print 'added to sys path',path

    #Discover plugins in path
    plugins = discover_plugin_in_paths()
                
    #Load plugins       
    load_plugins(plugins)

def find_plugins():
    return Plugin.__subclasses__()
