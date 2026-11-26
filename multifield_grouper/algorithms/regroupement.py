# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QVariant
from qgis.core import (
    NULL, QgsProcessing, QgsProcessingAlgorithm, QgsProcessingException,
    QgsProcessingParameterVectorLayer, QgsProcessingParameterField,
    QgsProcessingParameterString, QgsProcessingParameterFeatureSink,
    QgsFields, QgsField, QgsFeature, QgsWkbTypes,
)
from .. import core
from ..i18n import tr


class MultiFieldGroupingAlgorithm(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    FIELD_ID = "FIELD_ID"
    CATEGORY_FIELDS = "CATEGORY_FIELDS"
    SEPARATOR = "SEPARATOR"
    OUTPUT = "OUTPUT"

    def tr(self, text):
        return tr(text)

    def createInstance(self):
        return MultiFieldGroupingAlgorithm()

    def name(self):
        return "group_by_multiple_category_fields"

    def displayName(self):
        return tr("Group features by multiple category fields")

    def group(self):
        return tr("MultiField Grouper")

    def groupId(self):
        return "multifield_grouper"

    def shortHelpString(self):
        return tr(
            "Each selected category field is evaluated independently, so a feature may belong to several categories. Identifiers are unique within each category. Features with all category fields empty are collected in a special NULL category. Empty identifiers are ignored."
        )

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer(
            self.INPUT, tr("Input layer"),
            types=[QgsProcessing.SourceType.TypeVector],
        ))
        self.addParameter(QgsProcessingParameterField(
            self.FIELD_ID, tr("Identifier field"),
            parentLayerParameterName=self.INPUT,
        ))
        self.addParameter(QgsProcessingParameterField(
            self.CATEGORY_FIELDS, tr("Category fields"),
            parentLayerParameterName=self.INPUT, allowMultiple=True,
        ))
        self.addParameter(QgsProcessingParameterString(
            self.SEPARATOR, tr("Identifier list separator"), defaultValue=", ",
        ))
        self.addParameter(QgsProcessingParameterFeatureSink(
            self.OUTPUT, tr("Grouped summary table"),
        ))

    def processAlgorithm(self, parameters, context, feedback):
        layer = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        id_field = self.parameterAsString(parameters, self.FIELD_ID, context)
        category_fields = self.parameterAsFields(
            parameters, self.CATEGORY_FIELDS, context
        )
        separator = self.parameterAsString(parameters, self.SEPARATOR, context)

        if layer is None:
            raise QgsProcessingException(tr("Please select a valid input layer."))
        if not category_fields:
            raise QgsProcessingException(tr("Select at least one category field."))

        rows, stats = core.build_groups(
            layer.getFeatures(), id_field, category_fields, NULL
        )
        fields = QgsFields()
        fields.append(QgsField("categorie", QVariant.String))
        fields.append(QgsField("nb_elements", QVariant.Int))
        fields.append(QgsField("elements", QVariant.String))
        sink, destination = self.parameterAsSink(
            parameters, self.OUTPUT, context, fields,
            QgsWkbTypes.Type.NoGeometry, layer.crs(),
        )
        if sink is None:
            raise QgsProcessingException(tr("Could not create the output table."))

        total = max(1, len(rows))
        for index, (category, count, identifiers) in enumerate(rows):
            if feedback.isCanceled():
                break
            feature = QgsFeature(fields)
            feature.setAttributes([category, count, separator.join(identifiers)])
            sink.addFeature(feature)
            feedback.setProgress(int((index + 1) * 100 / total))

        feedback.pushInfo(tr("{0} categories created.").format(len(rows)))
        if stats["ignored_identifiers"]:
            feedback.pushWarning(
                tr("{0} feature(s) with an empty identifier were ignored.")
                .format(stats["ignored_identifiers"])
            )
        return {self.OUTPUT: destination}
