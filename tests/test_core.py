import unittest

from multifield_grouper.core import build_groups


class GroupingCoreTests(unittest.TestCase):
    def test_multiple_fields_are_independent_and_ids_are_unique(self):
        features = [
            {"id": " A ", "cat1": "North", "cat2": "Blue"},
            {"id": "A", "cat1": "North", "cat2": ""},
            {"id": "B", "cat1": "North", "cat2": None},
            {"id": "C", "cat1": "", "cat2": ""},
            {"id": " ", "cat1": "Ignored", "cat2": ""},
        ]
        rows, stats = build_groups(features, "id", ["cat1", "cat2"])
        self.assertEqual(rows, [
            ("Blue", 1, ["A"]),
            ("North", 2, ["A", "B"]),
            ("NULL", 1, ["C"]),
        ])
        self.assertEqual(stats["ignored_identifiers"], 1)
        self.assertEqual(stats["category_count"], 3)

    def test_literal_null_is_distinct_from_empty_category_bucket(self):
        features = [
            {"id": "1", "cat": "NULL"},
            {"id": "2", "cat": ""},
        ]
        rows, _ = build_groups(features, "id", ["cat"])
        self.assertEqual(rows, [
            ("NULL", 1, ["1"]),
            ("NULL (valeurs vides)", 1, ["2"]),
        ])

    def test_blank_categories_and_identifiers_are_trimmed_or_ignored(self):
        features = [
            {"id": " 17 ", "cat": "  A  "},
            {"id": None, "cat": "B"},
            {"id": "", "cat": ""},
        ]
        rows, stats = build_groups(features, "id", ["cat"])
        self.assertEqual(rows, [("A", 1, ["17"])])
        self.assertEqual(stats["ignored_identifiers"], 2)


if __name__ == "__main__":
    unittest.main()
