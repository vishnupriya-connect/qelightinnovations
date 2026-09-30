"""A deterministic batch selector using explicit position boundaries."""
from lab import sample


def select_batch(source, start, batch_size):
    """Return up to batch_size consecutive rows from the supplied table."""
    if type(start) is not int or type(batch_size) is not int:
        raise TypeError('start and batch_size must be Python integers')
    if start < 0:
        raise ValueError('start must be non-negative')
    if batch_size <= 0:
        raise ValueError('batch_size must be positive')
    return source.iloc[start:start + batch_size, :].copy()


if __name__ == '__main__':
    df = sample()
    for start in range(0, len(df), 2):
        batch = select_batch(df, start, 2)
        print(f'batch start={start}, rows={len(batch)}')
        print(batch.to_csv(index=True).strip())
    print('past end:', select_batch(df, 5, 2).shape)
