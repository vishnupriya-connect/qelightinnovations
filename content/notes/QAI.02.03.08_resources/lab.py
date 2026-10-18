import pandas as pd

from project import sample_data


df = sample_data()

comparison = df['score'] >= 80
print('comparison', comparison.tolist())
print('and', df.index[(df['score'] >= 80) & (df['attempts'] == 1)].tolist())
print('or', df.index[(df['track'] == 'SQL') | (df['score'] > 90)].tolist())
print('not', df.index[~(df['track'] == 'Cloud')].tolist())
print('isin', df.index[df['track'].isin(['Python', 'SQL'])].tolist())
print('isna', df.index[df['mentor'].isna()].tolist())
print('notna', df.index[df['mentor'].notna()].tolist())

reordered = pd.Series(
    [True, False, True, False, False, False],
    index=['L60', 'L50', 'L40', 'L30', 'L20', 'L10'],
)
print('aligned', df.loc[reordered, 'learner'].tolist())

nullable = pd.Series(
    [True, pd.NA, False, True, False, True], index=df.index, dtype='boolean'
)
print('nullable', df.loc[nullable, 'learner'].tolist())

failures = [
    lambda: (df['score'] >= 80) and df['active'],
    lambda: df['score'] >= 80 & df['attempts'] == 1,
    lambda: df.loc[[True, False]],
    lambda: df.loc[pd.Series([True, False], index=['X', 'Y'])],
]
for number, operation in enumerate(failures, start=1):
    try:
        operation()
    except Exception as error:
        print(f'failure_{number}', type(error).__name__)

variation_mask = (
    df['active']
    & (df['track'] == 'Python')
    & ((df['score'] < 90) | df['mentor'].isna())
)
print('variation')
print(df.loc[variation_mask, ['learner', 'score', 'mentor']].to_csv(index=True).strip())
