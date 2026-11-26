# -*- coding: utf-8 -*-
def classFactory(iface):
    from .plugin import MultiFieldGrouperPlugin
    return MultiFieldGrouperPlugin(iface)
