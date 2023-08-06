# A plugin generator

from .mini_plugin_generator import generate_mini_plugin


def generate(plugin_type, **params):
    """ Generates a directory with jana plugin.

    Known plugin types:
        mini_plugin

    Usual parameters:
        plugin_name - snake_case defined name (directory name will correspond to it)
        class_name  - CamelCase defined name (Related C++ class names will have this name)
        path        - Path to the directory with plugin, otherwise current dir is used

    """
    if plugin_type == "mini_plugin":
        return generate_mini_plugin(**params)