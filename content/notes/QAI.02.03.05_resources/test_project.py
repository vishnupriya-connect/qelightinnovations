import unittest
import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal
from lab import sample
from project import build_report


class ColumnSelectionTests(unittest.TestCase):
    def test_scalar_and_list_types(self):
        df = sample()
        self.assertIsInstance(df['python'], pd.Series)
        self.assertIsInstance(df[['python']], pd.DataFrame)
        self.assertEqual(df['python'].shape, (3,))
        self.assertEqual(df[['python']].shape, (3, 1))
        assert_series_equal(df.python, df['python'])

    def test_order_and_row_identity(self):
        df = sample()
        selected = df[['sql', 'student']]
        self.assertEqual(selected.columns.tolist(), ['sql', 'student'])
        self.assertEqual(selected.index.tolist(), ['s1', 's2', 's3'])
        self.assertEqual(selected['sql'].tolist(), [80, 77, 89])

    def test_rename_changes_headers_only(self):
        df = sample()
        renamed = df.rename(columns={'python': 'python_mark'}, errors='raise')
        self.assertEqual(df.columns.tolist(), ['student', 'python', 'sql', 'phone'])
        self.assertEqual(renamed['python_mark'].tolist(), [72, 85, 91])
        self.assertEqual(renamed.index.tolist(), df.index.tolist())
        self.assertEqual(renamed['python_mark'].dtype, df['python'].dtype)

    def test_header_replacement_is_positional(self):
        df = sample()[['sql', 'python']].copy()
        df.columns = ['first', 'second']
        self.assertEqual(df['first'].tolist(), [80, 77, 89])
        with self.assertRaises(ValueError):
            df.columns = ['one']

    def test_missing_selection_and_rename(self):
        df = sample()
        with self.assertRaises(KeyError):
            df[['student', 'Python']]
        with self.assertRaises(KeyError):
            df.rename(columns={'Python': 'mark'}, errors='raise')
        assert_frame_equal(df.rename(columns={'Python': 'mark'}), df)

    def test_attribute_collision_and_space(self):
        df = pd.DataFrame({'mean': [10], 'total mark': [30]})
        self.assertTrue(callable(df.mean))
        self.assertEqual(df['mean'].tolist(), [10])
        self.assertEqual(df['total mark'].tolist(), [30])

    def test_duplicate_label_exception(self):
        df = pd.DataFrame([[1, 2]], columns=['mark', 'mark'])
        self.assertIsInstance(df['mark'], pd.DataFrame)
        self.assertEqual(df['mark'].shape, (1, 2))

    def test_empty_selection_retains_rows(self):
        df = sample()
        self.assertEqual(df[[]].shape, (3, 0))
        self.assertEqual(df[[]].index.tolist(), df.index.tolist())

    def test_report_exact_values_and_privacy(self):
        expected = pd.DataFrame({
            'learner': ['Anu', 'Bala', 'Chitra'],
            'python_mark': [72, 85, 91], 'sql_mark': [80, 77, 89]
        }, index=['s1', 's2', 's3'])
        assert_frame_equal(build_report(sample()), expected)
        self.assertNotIn('phone', build_report(sample()).columns)

    def test_report_independent_and_source_preserved(self):
        source = sample()
        before = source.copy(deep=True)
        report = build_report(source)
        report['python_mark'] = [0, 0, 0]
        assert_frame_equal(source, before)

    def test_source_column_order_is_irrelevant(self):
        source = sample()[['phone', 'sql', 'python', 'student']]
        assert_frame_equal(build_report(source), build_report(sample()))

    def test_report_missing_required_column(self):
        with self.assertRaisesRegex(ValueError, 'Missing required columns'):
            build_report(sample()[['student', 'python']])

    def test_report_duplicate_headers_rejected(self):
        df = pd.DataFrame([['Anu', 72, 80, 99]], columns=['student', 'python', 'sql', 'sql'])
        with self.assertRaisesRegex(ValueError, 'must be unique'):
            build_report(df)

    def test_empty_source_valid_schema(self):
        empty = sample().head(0)
        self.assertEqual(build_report(empty).shape, (0, 3))
        self.assertEqual(build_report(empty).columns.tolist(), ['learner', 'python_mark', 'sql_mark'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
