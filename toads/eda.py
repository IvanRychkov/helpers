import numpy as np
import seaborn as sns
import pandas as pd
from IPython.display import display
from .image import Img
import matplotlib.pyplot as plt


def na_part(data, verbose=False):
    """Агрегирует долю пропусков в объектах pandas.

    verbose - печатает или возвращает значение
    """
    part = data.isna().sum() / len(data)
    if verbose:
        print('Доля пропусков в столбце "{}" равна {:.1%}'
              .format(data.name, part))
    else:
        return part


def describe(df):
    """Возвращает транспонированный describe()

    Добавляет строку с долей пропусков для каждого столбца.
    """
    return df.describe().append(df.agg([na_part])).transpose()


def dist_stats(column):
    """Возвращает словарь с характеристиками распределения:
    - Среднее
    - Медиана
    - Дисперсия
    - Стандартное отклонение
    """
    return {
        'mean': np.mean(column),
        'median': np.median(column),
        'var': np.var(column),
        'std': np.sqrt(np.var(column)),
    }


def first_look(df: pd.DataFrame(), scatter_matrix=True) -> None:
    """Выводит наиболее популярные сведения о датафрейме."""
    df.info()
    print('-' * 50)
    print('head()')
    display(df.head(3))
    print('-' * 50)
    print('nunique()')
    display(df.nunique())
    print('-' * 50)
    print('describe()')
    display(describe(df))
    print('-' * 50)
    print('corr()')
    display(df.corr())
    if scatter_matrix:
        sns.pairplot(df)
    print()


def print_shapes(*arrays):
    """Принимает список массивов и печатает их размеры."""
    for a in arrays:
        print(a.shape)


def plot_dist_classic(df, columns, dp_kws={}, bp_kws={}):
    """Рисует гистограммы и ящики с усами для каждого столбца датафрейма из списка."""
    for col in columns:
        with Img(f'Распределение признака "{col}"'):
            Img.subplot(2, 1, 1)
            sns.distplot(df[col], **dp_kws)
            Img.subplot(2, 1, 2)
            sns.boxplot(df[col], color='orange', **bp_kws)


def plot_time_series(data, n_ticks=15, plot_func=sns.lineplot, format_axis=True, **plot_kws):
    if not isinstance(data.index, pd.DatetimeIndex):
        raise TypeError('data.index must be instance of "pandas.DateTimeIndex".')
    if format_axis:
        ticks = np.linspace(0, data.shape[0] - 1, n_ticks).round().astype(int)
        # Берём названия дат из индекса
        labels = data.index[ticks]
        plt.xticks(ticks, labels)
        plt.gcf().autofmt_xdate()
    return plot_func(data=data.reset_index(), **plot_kws)


__all__ = ['describe', 'dist_stats', 'first_look', 'na_part',
           'plot_dist_classic', 'plot_time_series', 'print_shapes']
