import pandas as pd


def sample():
    return pd.DataFrame({
        'learner': ['Anu', 'Bala', 'Chitra', 'Deepa', 'Eshan'],
        'python': [72, 85, 91, 68, 88],
        'sql': [80, 77, 89, 75, 90],
    }, index=[40, 10, 70, 20, 60])


def run():
    df = sample()
    row = df.iloc[1]
    print('single:', type(row).__name__, row.name, row.shape)
    print('row values:', [row['learner'], int(row['python']), int(row['sql'])])
    print('one-row table:', type(df.iloc[[1]]).__name__, df.iloc[[1]].shape)
    print('list order:', df.iloc[[3, 0, 3]].index.tolist())
    print('range 1:4:', df.iloc[1:4].index.tolist())
    print('step ::2:', df.iloc[::2].index.tolist())
    print('last row:', df.iloc[-1].name, df.iloc[-1]['learner'])
    print('last two:', df.iloc[-2:].index.tolist())
    print('reverse:', df.iloc[::-1].index.tolist())
    block = df.iloc[1:4, [2, 0]]
    print('row and column block:')
    print(block.to_csv(index=True).strip())
    print('scalar cell:', int(df.iloc[2, 1]))
    print('one column:', type(df.iloc[:, 1]).__name__, df.iloc[:, 1].shape)
    print('one column table:', type(df.iloc[:, [1]]).__name__, df.iloc[:, [1]].shape)
    print('clipped slice:', df.iloc[3:99].index.tolist())
    print('empty slice:', df.iloc[5:99].shape)
    for label, action in [
        ('outside scalar', lambda: df.iloc[5]),
        ('outside list', lambda: df.iloc[[0, 5]]),
        ('too negative', lambda: df.iloc[-6]),
    ]:
        try:
            action()
        except IndexError:
            print(label + ': IndexError')
        else:
            raise AssertionError('Expected IndexError')
    try:
        df.iloc[::0]
    except ValueError:
        print('zero step: ValueError')
    else:
        raise AssertionError('Expected ValueError')
    print('variation:')
    print(df.iloc[0:5:2, [0, 2]].to_csv(index=False).strip())


if __name__ == '__main__':
    run()
