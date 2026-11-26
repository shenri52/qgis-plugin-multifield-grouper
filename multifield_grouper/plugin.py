# -*- coding: utf-8 -*-
import os
from qgis.PyQt.QtCore import QLocale
from qgis.PyQt.QtGui import QAction, QIcon
from .provider import MultiFieldGrouperProvider
from .gui.dialog import MultiFieldGrouperDialog


class MultiFieldGrouperPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.action = None
        self.provider = None

    def tr(self, text):
        if QLocale.system().name().lower().startswith("fr"):
            return {
                "Group features using several category fields": "Regrouper les entités avec plusieurs champs de catégorie",
                "&MultiField Grouper": "&MultiField Grouper",
            }.get(text, text)
        return text

    def initGui(self):
        icon_path = os.path.join(os.path.dirname(__file__), "icon.svg")
        icon = QIcon(icon_path) if os.path.isfile(icon_path) else QIcon()
        self.action = QAction(icon, "MultiField Grouper", self.iface.mainWindow())
        self.action.setObjectName("MultiFieldGrouperAction")
        self.action.setToolTip(self.tr("Group features using several category fields"))
        self.action.triggered.connect(self.run)
        self.iface.addPluginToMenu(self.tr("&MultiField Grouper"), self.action)
        self.iface.addToolBarIcon(self.action)

        self.provider = MultiFieldGrouperProvider()
        from qgis.core import QgsApplication
        QgsApplication.processingRegistry().addProvider(self.provider)

    def run(self):
        dialog = MultiFieldGrouperDialog(self.iface)
        execute = getattr(dialog, "exec", None) or dialog.exec_
        execute()

    def unload(self):
        if self.action is not None:
            self.iface.removePluginMenu(self.tr("&MultiField Grouper"), self.action)
            self.iface.removeToolBarIcon(self.action)
            self.action = None
        if self.provider is not None:
            from qgis.core import QgsApplication
            QgsApplication.processingRegistry().removeProvider(self.provider)
            self.provider = None
