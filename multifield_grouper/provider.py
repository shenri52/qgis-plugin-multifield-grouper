# -*- coding: utf-8 -*-
from qgis.core import QgsProcessingProvider

from .i18n import tr
from .algorithms.regroupement import MultiFieldGroupingAlgorithm


class MultiFieldGrouperProvider(QgsProcessingProvider):
    def loadAlgorithms(self):
        self.addAlgorithm(MultiFieldGroupingAlgorithm())

    def id(self):
        return "multifield_grouper"

    def name(self):
        return tr("MultiField Grouper")

    def longName(self):
        return self.name()
