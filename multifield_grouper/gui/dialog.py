# -*- coding: utf-8 -*-
import os
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QComboBox,
    QListWidget, QListWidgetItem, QLineEdit, QPushButton, QFileDialog,
    QMessageBox, QProgressBar,
)
from qgis.core import (
    NULL, QgsProject, QgsVectorLayer, QgsField, QgsFeature, QgsFields,
    QgsWkbTypes, QgsVectorFileWriter,
)
from qgis.PyQt.QtCore import QVariant
from .. import core
from ..i18n import is_french


TEXT = {
    "fr": {
        "title": "Regroupement multi-champs", "intro": "Regroupe les identifiants selon les valeurs de plusieurs champs de catégorie indépendants.",
        "layer": "Couche source", "id": "Champ identifiant", "categories": "Champs de catégorie (sélection multiple)",
        "separator": "Séparateur de la liste", "destination": "Destination", "memory": "Couche temporaire",
        "gpkg": "GeoPackage", "csv": "CSV", "file": "Fichier", "browse": "Parcourir…",
        "run": "Regrouper", "close": "Fermer", "choose": "Choisir un fichier de sortie",
        "need_fields": "Sélectionnez au moins un champ de catégorie.",
        "need_id": "Sélectionnez un champ identifiant.", "need_path": "Choisissez un fichier de sortie.",
        "done": "{0} catégorie(s) créée(s). {1} identifiant(s) vide(s) ignoré(s).",
        "error": "Échec du regroupement : ", "output": "Résultat MultiField Grouper",
    },
    "en": {
        "title": "MultiField Grouper", "intro": "Group identifiers using values from several independent category fields.",
        "layer": "Input layer", "id": "Identifier field", "categories": "Category fields (select multiple)",
        "separator": "List separator", "destination": "Output", "memory": "Temporary layer",
        "gpkg": "GeoPackage", "csv": "CSV", "file": "File", "browse": "Browse…",
        "run": "Group", "close": "Close", "choose": "Choose output file",
        "need_fields": "Select at least one category field.",
        "need_id": "Select an identifier field.", "need_path": "Choose an output file.",
        "done": "{0} categor(y/ies) created. {1} empty identifier(s) ignored.",
        "error": "Grouping failed: ", "output": "MultiField Grouper result",
    },
}


class MultiFieldGrouperDialog(QDialog):
    def __init__(self, iface):
        super().__init__(iface.mainWindow())
        self.iface = iface
        self.lang = "fr" if is_french() else "en"
        self.t = TEXT[self.lang]
        self.setWindowTitle(self.t["title"])
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "icon.svg")
        if os.path.isfile(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        self.setMinimumWidth(520)
        self._build_ui()
        self._populate_layers()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        intro = QLabel(self.t["intro"])
        intro.setWordWrap(True)
        layout.addWidget(intro)
        form = QFormLayout()
        self.layer_combo = QComboBox()
        self.layer_combo.currentIndexChanged.connect(self._populate_fields)
        form.addRow(self.t["layer"], self.layer_combo)
        self.id_combo = QComboBox()
        form.addRow(self.t["id"], self.id_combo)
        layout.addLayout(form)

        layout.addWidget(QLabel(self.t["categories"]))
        self.category_list = QListWidget()
        self.category_list.setMinimumHeight(150)
        layout.addWidget(self.category_list)

        self.separator_edit = QLineEdit(", ")
        form2 = QFormLayout()
        form2.addRow(self.t["separator"], self.separator_edit)
        self.output_combo = QComboBox()
        self.output_combo.addItem(self.t["memory"], "memory")
        self.output_combo.addItem(self.t["gpkg"], "gpkg")
        self.output_combo.addItem(self.t["csv"], "csv")
        self.output_combo.currentIndexChanged.connect(self._output_changed)
        form2.addRow(self.t["destination"], self.output_combo)
        file_row = QHBoxLayout()
        self.path_edit = QLineEdit()
        self.browse_button = QPushButton(self.t["browse"])
        self.browse_button.clicked.connect(self._browse)
        file_row.addWidget(self.path_edit, 1)
        file_row.addWidget(self.browse_button)
        form2.addRow(self.t["file"], file_row)
        layout.addLayout(form2)
        self.path_edit.setVisible(False)
        self.browse_button.setVisible(False)

        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.setVisible(False)
        layout.addWidget(self.progress)
        buttons = QHBoxLayout()
        buttons.addStretch(1)
        self.run_button = QPushButton(self.t["run"])
        self.run_button.clicked.connect(self._run)
        close_button = QPushButton(self.t["close"])
        close_button.clicked.connect(self.reject)
        buttons.addWidget(self.run_button)
        buttons.addWidget(close_button)
        layout.addLayout(buttons)

    def _populate_layers(self):
        self.layer_combo.clear()
        for layer in QgsProject.instance().mapLayers().values():
            if isinstance(layer, QgsVectorLayer) and layer.isValid():
                self.layer_combo.addItem(layer.name(), layer.id())
        self._populate_fields()

    def _layer(self):
        layer_id = self.layer_combo.currentData()
        return QgsProject.instance().mapLayer(layer_id) if layer_id else None

    def _populate_fields(self, *_):
        layer = self._layer()
        self.id_combo.clear()
        self.category_list.clear()
        if not layer:
            return
        names = [field.name() for field in layer.fields()]
        self.id_combo.addItems(names)
        for name in names:
            item = QListWidgetItem(name, self.category_list)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)

    def _output_changed(self, *_):
        needs_file = self.output_combo.currentData() in ("gpkg", "csv")
        self.path_edit.setVisible(needs_file)
        self.browse_button.setVisible(needs_file)

    def _browse(self):
        kind = self.output_combo.currentData()
        extension = ".gpkg" if kind == "gpkg" else ".csv"
        path, _ = QFileDialog.getSaveFileName(
            self, self.t["choose"], "", "GeoPackage (*.gpkg)" if kind == "gpkg" else "CSV (*.csv)")
        if path:
            if not path.lower().endswith(extension):
                path += extension
            self.path_edit.setText(path)

    def _run(self):
        layer = self._layer()
        if not layer or not self.id_combo.currentText():
            QMessageBox.warning(self, self.windowTitle(), self.t["need_id"])
            return
        category_fields = [
            self.category_list.item(i).text()
            for i in range(self.category_list.count())
            if self.category_list.item(i).checkState() == Qt.CheckState.Checked
        ]
        if not category_fields:
            QMessageBox.warning(self, self.windowTitle(), self.t["need_fields"])
            return
        kind = self.output_combo.currentData()
        path = self.path_edit.text().strip()
        if kind != "memory" and not path:
            QMessageBox.warning(self, self.windowTitle(), self.t["need_path"])
            return

        self.run_button.setEnabled(False)
        self.progress.setVisible(True)
        try:
            rows, stats = core.build_groups(
                layer.getFeatures(), self.id_combo.currentText(), category_fields, NULL)
            fields = QgsFields()
            fields.append(QgsField("categorie", QVariant.String))
            fields.append(QgsField("nb_elements", QVariant.Int))
            fields.append(QgsField("elements", QVariant.String))
            result = QgsVectorLayer("None", self.t["output"], "memory")
            provider = result.dataProvider()
            provider.addAttributes(list(fields))
            result.updateFields()
            features = []
            separator = self.separator_edit.text()
            for category, count, identifiers in rows:
                feature = QgsFeature(result.fields())
                feature.setAttributes([category, count, separator.join(identifiers)])
                features.append(feature)
            provider.addFeatures(features)
            result.updateExtents()

            if kind == "memory":
                QgsProject.instance().addMapLayer(result)
            else:
                options = QgsVectorFileWriter.SaveVectorOptions()
                options.driverName = "GPKG" if kind == "gpkg" else "CSV"
                options.fileEncoding = "UTF-8"
                if kind == "csv":
                    options.layerOptions = ["GEOMETRY=AS_WKT"]
                error, message, output_path, _ = QgsVectorFileWriter.writeAsVectorFormatV3(
                    result, path, QgsProject.instance().transformContext(), options)
                if error != QgsVectorFileWriter.WriterError.NoError:
                    raise RuntimeError(message)
                saved = QgsVectorLayer(output_path, os.path.splitext(os.path.basename(path))[0], "ogr")
                if saved.isValid():
                    QgsProject.instance().addMapLayer(saved)
            QMessageBox.information(
                self, self.windowTitle(),
                self.t["done"].format(stats["category_count"], stats["ignored_identifiers"]))
            self.accept()
        except Exception as exc:
            QMessageBox.critical(self, self.windowTitle(), self.t["error"] + str(exc))
        finally:
            self.progress.setVisible(False)
            self.run_button.setEnabled(True)
