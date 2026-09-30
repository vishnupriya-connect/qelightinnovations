import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
from lab import sample
from project import select_batch


class PositionTests(unittest.TestCase):
    def test_position_is_not_label(self):
        df = sample()
        self.assertEqual(df.iloc[1].name, 10)
        self.assertEqual(df.iloc[1]['learner'], 'Bala')
        with self.assertRaises(IndexError):
            df.iloc[10]

    def test_scalar_vs_list_shape(self):
        df = sample()
        self.assertIsInstance(df.iloc[1], pd.Series)
        self.assertIsInstance(df.iloc[[1]], pd.DataFrame)
        self.assertEqual(df.iloc[[1]].shape, (1, 3))

    def test_list_order_and_duplicates(self):
        result = sample().iloc[[3, 0, 3]]
        self.assertEqual(result.index.tolist(), [20, 40, 20])
        self.assertEqual(result['learner'].tolist(), ['Deepa', 'Anu', 'Deepa'])

    def test_exclusive_stop_and_step(self):
        df = sample()
        self.assertEqual(df.iloc[1:4].index.tolist(), [10, 70, 20])
        self.assertEqual(df.iloc[::2].index.tolist(), [40, 70, 60])

    def test_negative_positions_and_reverse(self):
        df = sample()
        self.assertEqual(df.iloc[-1].name, 60)
        self.assertEqual(df.iloc[-2:].index.tolist(), [20, 60])
        self.assertEqual(df.iloc[::-1].index.tolist(), [60, 20, 70, 10, 40])

    def test_two_axis_selection(self):
        block = sample().iloc[1:4, [2, 0]]
        self.assertEqual(block.columns.tolist(), ['sql', 'learner'])
        self.assertEqual(block.index.tolist(), [10, 70, 20])
        self.assertEqual(block['sql'].tolist(), [77, 89, 75])
        self.assertEqual(sample().iloc[2, 1], 91)

    def test_column_dimension(self):
        df = sample()
        self.assertEqual(df.iloc[:, 1].shape, (5,))
        self.assertEqual(df.iloc[:, [1]].shape, (5, 1))

    def test_bounds_and_empty_slice(self):
        df = sample()
        for key in [5, -6, [0, 5]]:
            with self.assertRaises(IndexError):
                df.iloc[key]
        self.assertEqual(df.iloc[3:99].index.tolist(), [20, 60])
        self.assertEqual(df.iloc[5:99].shape, (0, 3))
        with self.assertRaises(ValueError):
            df.iloc[::0]

    def test_batch_exact_rows(self):
        expected = pd.DataFrame({'learner': ['Chitra', 'Deepa'],
            'python': [91, 68], 'sql': [89, 75]}, index=[70, 20])
        assert_frame_equal(select_batch(sample(), 2, 2), expected)

    def test_final_batch_and_past_end(self):
        df = sample()
        self.assertEqual(select_batch(df, 4, 2).index.tolist(), [60])
        self.assertEqual(select_batch(df, 5, 2).shape, (0, 3))
        self.assertEqual(select_batch(df, 99, 2).shape, (0, 3))

    def test_batches_partition_source(self):
        df = sample()
        batches = [select_batch(df, start, 2) for start in range(0, len(df), 2)]
        assert_frame_equal(pd.concat(batches), df)

    def test_batch_independent_copy(self):
        df = sample()
        before = df.copy(deep=True)
        batch = select_batch(df, 0, 2)
        batch['python'] = [0, 0]
        assert_frame_equal(df, before)

    def test_invalid_arguments(self):
        for start, size in [(-1, 2), (0, 0), (0, -1)]:
            with self.assertRaises(ValueError):
                select_batch(sample(), start, size)
        for start, size in [(1.5, 2), (True, 2), (0, '2'), (0, False)]:
            with self.assertRaises(TypeError):
                select_batch(sample(), start, size)

    def test_empty_source_schema(self):
        empty = sample().head(0)
        assert_frame_equal(select_batch(empty, 0, 2), empty)


if __name__ == '__main__':
    unittest.main(verbosity=2)
