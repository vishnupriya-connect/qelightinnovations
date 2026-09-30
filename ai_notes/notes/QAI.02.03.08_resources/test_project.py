import unittest

import pandas as pd
from pandas.testing import assert_frame_equal

from project import build_review_queue, sample_data


class ReviewQueueTests(unittest.TestCase):
    def setUp(self):
        self.df = sample_data()

    def test_exact_result_with_unassigned(self):
        actual = build_review_queue(self.df, ['Python', 'SQL'], 80, True)
        expected = self.df.loc[
            ['L20', 'L30', 'L50', 'L60'], ['learner', 'track', 'score', 'mentor']
        ].copy()
        assert_frame_equal(actual, expected)

    def test_default_excludes_unassigned(self):
        actual = build_review_queue(self.df, ['Python', 'SQL'], 80)
        self.assertEqual(actual.index.tolist(), ['L30', 'L60'])

    def test_threshold_is_inclusive(self):
        actual = build_review_queue(self.df, ['Python'], 80, True)
        self.assertIn('L60', actual.index)

    def test_no_matches_has_valid_schema(self):
        actual = build_review_queue(self.df, ['Cloud'], 100, True)
        self.assertEqual(actual.shape, (0, 4))
        self.assertEqual(actual.columns.tolist(), ['learner', 'track', 'score', 'mentor'])

    def test_source_order_is_preserved(self):
        actual = build_review_queue(self.df, ['SQL', 'Python'], 80, True)
        self.assertEqual(actual.index.tolist(), ['L20', 'L30', 'L50', 'L60'])

    def test_membership_excludes_other_tracks(self):
        actual = build_review_queue(self.df, ['SQL'], 0, True)
        self.assertEqual(actual.index.tolist(), ['L20', 'L50'])

    def test_missing_columns(self):
        with self.assertRaisesRegex(ValueError, 'Missing required columns'):
            build_review_queue(self.df.drop(columns='mentor'), ['Python'], 0)

    def test_duplicate_index(self):
        broken = self.df.copy()
        broken.index = ['X', 'X', 'A', 'B', 'C', 'D']
        with self.assertRaisesRegex(ValueError, 'unique'):
            build_review_queue(broken, ['Python'], 0)

    def test_empty_tracks(self):
        with self.assertRaisesRegex(ValueError, 'must not be empty'):
            build_review_queue(self.df, [], 0)

    def test_duplicate_tracks(self):
        with self.assertRaisesRegex(ValueError, 'duplicates'):
            build_review_queue(self.df, ['SQL', 'SQL'], 0)

    def test_invalid_threshold_string(self):
        with self.assertRaises(TypeError):
            build_review_queue(self.df, ['SQL'], '80')

    def test_invalid_threshold_boolean(self):
        with self.assertRaises(TypeError):
            build_review_queue(self.df, ['SQL'], True)

    def test_invalid_flag(self):
        with self.assertRaises(TypeError):
            build_review_queue(self.df, ['SQL'], 80, 1)

    def test_non_numeric_score(self):
        broken = self.df.assign(score=self.df['score'].astype(str))
        with self.assertRaises(TypeError):
            build_review_queue(broken, ['SQL'], 80)

    def test_missing_score(self):
        broken = self.df.copy()
        broken.loc['L10', 'score'] = float('nan')
        with self.assertRaisesRegex(ValueError, 'missing'):
            build_review_queue(broken, ['Python'], 80)

    def test_non_boolean_active(self):
        broken = self.df.assign(active=[1, 1, 1, 0, 1, 1])
        with self.assertRaisesRegex(TypeError, 'Boolean'):
            build_review_queue(broken, ['Python'], 80)

    def test_source_unchanged_and_result_independent(self):
        before = self.df.copy(deep=True)
        result = build_review_queue(self.df, ['Python', 'SQL'], 80, True)
        result.loc[:, 'score'] = 0
        assert_frame_equal(self.df, before)


if __name__ == '__main__':
    unittest.main(verbosity=2)
