"""Column selection, ordering, and safe header changes."""
import pandas as pd


def sample():
    return pd.DataFrame({
        'student': ['Anu', 'Bala', 'Chitra'],
        'python': [72, 85, 91],
        'sql': [80, 77, 89],
        'phone': ['private-a', 'private-b', 'private-c'],
    }, index=['s1', 's2', 's3'])


def run():
    df = sample()
    score = df['python']
    table = df[['python']]
    print('single:', type(score).__name__, score.shape, score.tolist())
    print('one-column table:', type(table).__name__, table.shape)
    print('attribute equals brackets:', df.python.equals(score))
    requested = ['sql', 'student', 'python']
    selected = df[requested]
    print('ordered columns:', selected.columns.tolist())
    print(selected.to_csv(index=True).strip())
    renamed = selected.rename(columns={'student': 'learner', 'python': 'python_mark'}, errors='raise')
    print('renamed:', renamed.columns.tolist())
    print('original:', df.columns.tolist())
    replaced = selected.copy()
    replaced.columns = ['sql_mark', 'learner', 'python_mark']
    print('replaced:', replaced.columns.tolist())
    variation = df[['student', 'sql']].rename(columns={'sql': 'database_mark'}, errors='raise')
    print('variation:')
    print(variation.to_csv(index=False).strip())
    for label, action in [
        ('missing selection', lambda: df[['student', 'Python']]),
        ('strict rename', lambda: df.rename(columns={'Python': 'python_mark'}, errors='raise')),
    ]:
        try:
            action()
        except KeyError:
            print(label + ': KeyError')
        else:
            raise AssertionError('Expected KeyError')
    try:
        replaced.columns = ['only_one']
    except ValueError:
        print('wrong header count: ValueError')
    else:
        raise AssertionError('Expected ValueError')
    collision = pd.DataFrame({'mean': [10, 20], 'total mark': [30, 40]})
    print('mean attribute callable:', callable(collision.mean))
    print('mean column:', collision['mean'].tolist())
    print('space label:', collision['total mark'].tolist())
    duplicate = pd.DataFrame([[1, 2]], columns=['mark', 'mark'])
    print('duplicate scalar selection:', type(duplicate['mark']).__name__, duplicate['mark'].shape)
    empty = df[[]]
    print('empty column selection:', empty.shape, empty.index.tolist())


if __name__ == '__main__':
    run()
