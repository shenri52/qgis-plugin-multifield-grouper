# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.core import (
    NULL, QgsProcessing, QgsProcessingAlgorithm, QgsProcessingException,
    QgsProcessingParameterVectorLayer, QgsProcessingParameterField,
    QgsProcessingParameterString, QgsProcessingParameterFeatureSink,
    QgsFields, QgsField, QgsFeature, QgsWkbTypes,
)
from .. import core


class MultiFieldGroupingAlgorithm(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    FIELD_ID = "FIELD_ID"
    CATEGORY_FIELDS = "CATEGORY_FIELDS"
    SEPARATOR = "SEPARATOR"
    OUTPUT = "OUTPUT"

    def tr(self, text):
        return QCoreApplication.translate("MultiFieldGrouper", text)

    def createInstance(self):
        return MultiFieldGroupingAlgorithm()

    def name(self):
        return "group_by_multiple_category_fields"

    def displayName(self):
        return self.tr("Group features by multiple category fields")

    def group(self):
        return self.tr("MultiField Grouper")

    def groupId(self):
        return "multifield_grouper"

    def shortHelpString(self):
        return self.tr(
            "Each selected category field is evaluated independently, so a "
            "feature may belong to several categories. Identifiers are unique "
            "within each category. Features with all category fields empty "
            "are collected in a special NULL category. Empty identifiers are ignored."
        )

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer(
            self.INPUT, self.tr("Input layer"), types=[QgsProcessing.TypeVector]))
        self.addParameter(QgsProcessingParameterField(
            self.FIELD_ID, self.tr("Identifier field"),
            parentLayerParameterName=self.INPUT))
        self.addParameter(QgsProcessingParameterField(
            self.CATEGORY_FIELDS, self.tr("Category fields"),
            parentLayerParameterName=self.INPUT, allowMultiple=True))
        self.addParameter(QgsProcessingParameterString(
            self.SEPARATOR, self.tr("Identifier list separator"), defaultValue=", "))
        self.addParameter(QgsProcessingParameterFeatureSink(
            self.OUTPUT, self.tr("Grouped summary table")))

    def processAlgorithm(self, parameters, context, feedback):
        layer = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        id_field = self.parameterAsString(parameters, self.FIELD_ID, context)
        category_fields = self.parameterAsFields(parameters, self.CATEGORY_FIELDS, context)
        separator = self.parameterAsString(parameters, self.SEPARATOR, context)

        if layer is None:
            raise QgsProcessingException(self.tr("Please select a valid input layer."))
        if not category_fields:
            raise QgsProcessingException(self.tr("Select at least one category field."))

        rows, stats = core.build_groups(layer.getFeatures(), id_field, category_fields, NULL)
        fields = QgsFields()
        fields.append(QgsField("categorie", QVariant.String))
        fields.append(QgsField("nb_elements", QVariant.Int))
        fields.append(QgsField("elements", QVariant.String))

        sink, destination = self.parameterAsSink(
            parameters, self.OUTPUT, context, fields,
            QgsWkbTypes.NoGeometry, layer.crs())
        if sink is None:
            raise QgsProcessingException(self.tr("Could not create the output table."))

        total = max(1, len(rows))
        for index, (category, count, identifiers) in enumerate(rows):
            if feedback.isCanceled():
                break
            feature = QgsFeature(fields)
            feature.setAttributes([category, count, separator.join(identifiers)])
            sink.addFeature(feature)
            feedback.setProgress(int((index + 1) * 100 / total))

        feedback.pushInfo(self.tr("{0} categories created.").format(len(rows)))
        if stats["ignored_identifiers"]:
            feedback.pushWarning(self.tr("{0} feature(s) with an empty identifier were ignored.").format(
                stats["ignored_identifiers"]))
        return {self.OUTPUT: destination}
