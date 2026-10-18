from numbers import Real

import pandas as pd


def build_review_queue(source, allowed_tracks, minimum_score, include_unassigned=False):
    required = ['learner', 'track', 'score', 'mentor', 'active']
    missing = [name for name in required if name not in source.columns]
    if missing:
        raise ValueError(f'Missing required columns: {missing}')
    if not source.index.is_unique:
        raise ValueError('Source row labels must be unique')

    tracks = list(allowed_tracks)
    if not tracks:
        raise ValueError('allowed_tracks must not be empty')
    if len(tracks) != len(set(tracks)):
        raise ValueError('allowed_tracks must not contain duplicates')
    if isinstance(minimum_score, bool) or not isinstance(minimum_score, Real):
        raise TypeError('minimum_score must be a real number')
    if not isinstance(include_unassigned, bool):
        raise TypeError('include_unassigned must be Boolean')
    if not pd.api.types.is_numeric_dtype(source['score']):
        raise TypeError('score must be numeric')
    if source['score'].isna().any():
        raise ValueError('score must not contain missing values')
    if not pd.api.types.is_bool_dtype(source['active']):
        raise TypeError('active must be Boolean')

    mask = (
        source['active']
        & source['track'].isin(tracks)
        & source['score'].ge(minimum_score)
    )
    if not include_unassigned:
        mask &= source['mentor'].notna()
    return source.loc[mask, ['learner', 'track', 'score', 'mentor']].copy()


def sample_data():
    return pd.DataFrame(
        {
            'learner': ['Anu', 'Bala', 'Chitra', 'Deepa', 'Eshan', 'Farah'],
            'track': ['Python', 'SQL', 'Python', 'Cloud', 'SQL', 'Python'],
            'score': [72, 85, 91, 68, 88, 80],
            'attempts': [1, 2, 1, 3, 2, 1],
            'mentor': ['Mira', None, 'Ravi', 'Mira', pd.NA, 'Ravi'],
            'active': [True, True, True, False, True, True],
        },
        index=['L10', 'L20', 'L30', 'L40', 'L50', 'L60'],
    )


if __name__ == '__main__':
    result = build_review_queue(sample_data(), ['Python', 'SQL'], 80, True)
    print(result.to_csv(index=True).strip())
