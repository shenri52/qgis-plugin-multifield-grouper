# -*- coding: utf-8 -*-
"""System-locale based translations shared by the plugin interface."""

from qgis.PyQt.QtCore import QLocale


_FR = {
    "MultiField Grouper": "Regroupement multi-champs",
    "&MultiField Grouper": "&Regroupement multi-champs",
    "Group features using several category fields":
        "Regrouper les entités à l'aide de plusieurs champs de catégorie",
    "Group features by multiple category fields":
        "Regrouper les entités par plusieurs champs de catégorie",
    "Each selected category field is evaluated independently, so a feature may belong to several categories. Identifiers are unique within each category. Features with all category fields empty are collected in a special NULL category. Empty identifiers are ignored.":
        "Chaque champ de catégorie sélectionné est analysé indépendamment : une entité peut appartenir à plusieurs catégories. Les identifiants sont uniques dans chaque catégorie. Les entités dont tous les champs de catégorie sont vides sont regroupées dans une catégorie spéciale NULL. Les identifiants vides sont ignorés.",
    "Input layer": "Couche source",
    "Identifier field": "Champ identifiant",
    "Category fields": "Champs de catégorie",
    "Identifier list separator": "Séparateur de la liste des identifiants",
    "Grouped summary table": "Table récapitulative",
    "Please select a valid input layer.": "Veuillez sélectionner une couche source valide.",
    "Select at least one category field.": "Veuillez sélectionner au moins un champ de catégorie.",
    "Could not create the output table.": "Impossible de créer la table de sortie.",
    "{0} categories created.": "{0} catégorie(s) créée(s).",
    "{0} feature(s) with an empty identifier were ignored.":
        "{0} entité(s) avec un identifiant vide ont été ignorées.",
}


def is_french():
    """Return whether the system locale is French."""
    return QLocale.system().name().lower().startswith("fr")


def tr(text):
    """Translate a source string when the system locale is French."""
    return _FR.get(text, text) if is_french() else text
