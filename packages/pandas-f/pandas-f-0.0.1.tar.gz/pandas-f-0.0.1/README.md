# pandas_f
Plugin that adds naïve flatmap to pandas.

The purpose is to provide a `map` function
to both `pd.DataFrame` and `pd.Series`
that applies any function
that maps a `pd.DataFrame` or `pd.Series` into `pd.DataFrame`,
and returns concatenated results as a single `pd.DataFrame`.

In other words, this plugin aims to provide
a `fmap` function in the category
of `typing.Union[pd.Series, pd.DataFrame]`.

Example:

    >>> import pandas, pandas_f
    >>> def fn(df: pd.DataFrame) -> pd.DataFrame:
    ...     c = df['a'] + 1
    ...     d = df['a'] + df['b']
    ...     return pd.DataFrame({'c': c, 'd': d})
    >>> input_df = pd.DataFrame([
    ...     {'a': 1, 'b': 2},
    ...     {'a': 2, 'b': 3},
    ...     {'a': 3, 'b': 4},
    ... ])
    >>> input_df.f.map(fn)
       c  d
    0  2  3
    1  3  5
    2  4  7

## Install

    pip install pandas-f

## Usage

Just import `pandas_f` to make `.f` extension available.
