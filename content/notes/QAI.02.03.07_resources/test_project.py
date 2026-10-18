import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
from lab import sample
from project import learner_report


class LabelSelectionTests(unittest.TestCase):
    def test_label_is_not_position(self):
        df = sample()
        self.assertEqual(df.loc["L10"].name, "L10")
        self.assertEqual(df.loc["L10"]["learner"], "Bala")

    def test_scalar_and_list_dimensions(self):
        df = sample()
        self.assertIsInstance(df.loc["L10"], pd.Series)
        self.assertIsInstance(df.loc[["L10"]], pd.DataFrame)
        self.assertEqual(df.loc[["L10"]].shape, (1, 3))

    def test_list_order_and_repetition(self):
        result = sample().loc[["L20", "L40", "L20"]]
        self.assertEqual(result.index.tolist(), ["L20", "L40", "L20"])
        self.assertEqual(result["learner"].tolist(), ["Deepa", "Anu", "Deepa"])

    def test_label_slice_is_inclusive_and_order_based(self):
        df = sample()
        self.assertEqual(df.loc["L10":"L20"].index.tolist(), ["L10", "L70", "L20"])
        self.assertEqual(df.loc["L20":"L10":-1].index.tolist(), ["L20", "L70", "L10"])

    def test_two_axis_selection(self):
        block = sample().loc[["L70", "L10"], ["sql", "learner"]]
        self.assertEqual(block.index.tolist(), ["L70", "L10"])
        self.assertEqual(block.columns.tolist(), ["sql", "learner"])
        self.assertEqual(block["sql"].tolist(), [89, 77])
        self.assertEqual(sample().loc["L70", "python"], 91)

    def test_column_dimension(self):
        df = sample()
        self.assertEqual(df.loc[:, "python"].shape, (5,))
        self.assertEqual(df.loc[:, ["python"]].shape, (5, 1))

    def test_missing_labels_raise(self):
        df = sample()
        for operation in [
            lambda: df.loc["L99"],
            lambda: df.loc[["L10", "L99"]],
            lambda: df.loc["L10", "Python"],
        ]:
            with self.assertRaises(KeyError):
                operation()

    def test_duplicate_index_changes_scalar_shape(self):
        df = pd.DataFrame({"mark": [70, 80, 90]}, index=["A", "A", "B"])
        self.assertIsInstance(df.loc["A"], pd.DataFrame)
        self.assertEqual(df.loc["A"].shape, (2, 1))

    def test_report_exact_values(self):
        expected = pd.DataFrame(
            {"learner": ["Chitra", "Bala"], "python": [91, 85], "sql": [89, 77]},
            index=["L70", "L10"],
        )
        assert_frame_equal(learner_report(sample(), ["L70", "L10"]), expected)

    def test_report_preserves_request_order(self):
        self.assertEqual(learner_report(sample(), ["L60", "L40"]).index.tolist(), ["L60", "L40"])

    def test_report_copy_is_independent(self):
        source = sample()
        before = source.copy(deep=True)
        report = learner_report(source, ["L40", "L10"])
        report["python"] = [0, 0]
        assert_frame_equal(source, before)

    def test_unknown_and_duplicate_requests_rejected(self):
        with self.assertRaisesRegex(ValueError, "Unknown learner"):
            learner_report(sample(), ["L10", "L99"])
        with self.assertRaisesRegex(ValueError, "Requested learner"):
            learner_report(sample(), ["L10", "L10"])

    def test_duplicate_source_index_rejected(self):
        source = sample()
        source.index = ["A", "A", "C", "D", "E"]
        with self.assertRaisesRegex(ValueError, "Source row labels"):
            learner_report(source, ["A"])

    def test_missing_column_rejected(self):
        with self.assertRaisesRegex(ValueError, "Missing required columns"):
            learner_report(sample().drop(columns="sql"), ["L10"])

    def test_empty_request_and_empty_source(self):
        result = learner_report(sample(), [])
        self.assertEqual(result.shape, (0, 3))
        empty = sample().head(0)
        assert_frame_equal(learner_report(empty, []), empty)


if __name__ == "__main__":
    unittest.main(verbosity=2)
