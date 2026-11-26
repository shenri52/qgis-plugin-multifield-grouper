# -*- coding: utf-8 -*-
import os

from qgis.PyQt.QtGui import QAction, QIcon
from qgis.core import QgsApplication

from .i18n import tr
from .provider import MultiFieldGrouperProvider
from .gui.dialog import MultiFieldGrouperDialog


class MultiFieldGrouperPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.action = None
        self.provider = None
        self.menu_name = tr("&MultiField Grouper")

    def initGui(self):
        icon_path = os.path.join(os.path.dirname(__file__), "icon.svg")
        icon = QIcon(icon_path) if os.path.isfile(icon_path) else QIcon()
        self.action = QAction(tr("MultiField Grouper"), self.iface.mainWindow())
        if not icon.isNull():
            self.action.setIcon(icon)
        self.action.setObjectName("MultiFieldGrouperAction")
        self.action.setToolTip(tr("Group features using several category fields"))
        self.action.triggered.connect(self.run)
        self.iface.addPluginToMenu(self.menu_name, self.action)
        self.iface.addToolBarIcon(self.action)

        self.provider = MultiFieldGrouperProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def run(self):
        dialog = MultiFieldGrouperDialog(self.iface)
        execute = getattr(dialog, "exec", None) or dialog.exec_
        execute()

    def unload(self):
        if self.action is not None:
            self.iface.removePluginMenu(self.menu_name, self.action)
            self.iface.removeToolBarIcon(self.action)
            self.action = None
        if self.provider is not None:
            QgsApplication.processingRegistry().removeProvider(self.provider)
            self.provider = None
