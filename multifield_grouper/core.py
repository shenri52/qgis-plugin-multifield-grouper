# -*- coding: utf-8 -*-
"""Shared grouping engine. Kept independent from QGIS and Qt."""
from collections import defaultdict

MISSING_CATEGORY = object()
MISSING_LABEL = "NULL"


def is_empty(value, qgis_null=None):
    """Return True for None, QGIS NULL, and whitespace-only values."""
    if value is None:
        return True
    if qgis_null is not None:
        try:
            if value == qgis_null:
                return True
        except Exception:
            pass
    return str(value).strip() == ""


def build_groups(features, id_field, category_fields, qgis_null=None):
    """Return sorted (category, count, identifiers) rows and processing stats."""
    groups = defaultdict(set)
    ignored_ids = 0
    processed = 0

    for feature in features:
        processed += 1
        raw_id = feature[id_field]
        if is_empty(raw_id, qgis_null):
            ignored_ids += 1
            continue
        identifier = str(raw_id).strip()
        has_category = False

        for field_name in category_fields:
            value = feature[field_name]
            if is_empty(value, qgis_null):
                continue
            groups[str(value).strip()].add(identifier)
            has_category = True

        if not has_category:
            groups[MISSING_CATEGORY].add(identifier)

    rows = []
    keys = sorted(
        (key for key in groups if key is not MISSING_CATEGORY),
        key=lambda value: (value.casefold(), value)
    )
    for category in keys:
        rows.append((category, len(groups[category]), sorted(groups[category])))

    if MISSING_CATEGORY in groups:
        # Keep a literal category named "NULL" distinct from missing values.
        missing_label = MISSING_LABEL
        if MISSING_LABEL in groups:
            missing_label = "NULL (valeurs vides)"
            suffix = 2
            while missing_label in groups:
                missing_label = "NULL (valeurs vides {0})".format(suffix)
                suffix += 1
        rows.append((missing_label, len(groups[MISSING_CATEGORY]),
                     sorted(groups[MISSING_CATEGORY])))

    return rows, {
        "features": processed,
        "ignored_identifiers": ignored_ids,
        "category_count": len(rows),
    }


def output_fields():
    return ("categorie", "nb_elements", "elements")
