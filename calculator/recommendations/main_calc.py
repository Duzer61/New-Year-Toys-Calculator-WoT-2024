import pandas as pd
from calc.constants import (ALL_RANDOM_CRAFT, ALL_SPECIFIC_CRAFT,
                            COLLECTIONS_NUM, FULL_COLLECTION_DATA,
                            HALF_SPECIFIC_CRAFT, MAX_TOYS_IN_COLLECTION,
                            ONE_TOY_FRAGMENTS, TOTAL_TOYS)
from calc.models import UserAlbums

from .models import AlbumSelect

full_df = pd.DataFrame(
    {
        'national': FULL_COLLECTION_DATA,
        'eastern': FULL_COLLECTION_DATA,
        'magic': FULL_COLLECTION_DATA,
        'christmas': FULL_COLLECTION_DATA,
    }
)

ALBUMS = ['national', 'eastern', 'magic', 'christmas']
ITEMS = ['hanging', 'crown', 'gift', 'garland']


def get_user_df(album):
    """
    Возвращает DataFrame pandas для коллекции пользователя.
    """
    album_data = {}
    for album_type in ALBUMS:
        album_data[album_type] = {}
        for item in ITEMS:
            element_name = f'{album_type}_{item}'
            album_data[album_type][item] = getattr(album, element_name)
    user_df = pd.DataFrame(album_data)
    return user_df


def get_actual_df(user_df, album_select):
    """
    Возвращает датафрейм с актуальными альбомами (которые пользователь
    выбрал для крафта) и список актуальных альбомов.
    """
    if album_select.toggle:
        actual_albums = [
            album for album in ALBUMS if getattr(album_select, album)
        ]
        actual_df = user_df[actual_albums]  # Урезаем датафрейм
    else:
        actual_df = user_df
        actual_albums = ALBUMS
    return actual_df, actual_albums


def get_min_data(average_fragments_num, actual_albums=None):
    """
    Возвращает значение минимального количества осколков на крафт
    по коллекциям или по категориям, а так-же имена коллекций или
    категорий с этим значением.
    """
    # Исключаем из сравнения строки ('пропуск')
    if average_fragments_num.ndim == 1:  # Вычисления для одномерн. датафрейма
        numeric_values = pd.to_numeric(average_fragments_num, errors='coerce')
        min_value = numeric_values.min()
        min_names = average_fragments_num[
            average_fragments_num == min_value
        ].index.to_list()
    else:  # Вычисления для двумерного датафрейма
        columns_to_drop = average_fragments_num.columns[
            ~average_fragments_num.columns.isin(actual_albums)
        ]
        average_fragments_num_drop = average_fragments_num.drop(
            columns_to_drop, axis=1
        )
        # Минимальное количество осколков на крафт и
        # коллекции-категории соответственно
        min_value = average_fragments_num_drop.min().min()
        min_names = average_fragments_num_drop[
            average_fragments_num_drop == min_value
        ].stack().index.tolist()

    min_data = {
        'min_value': min_value,
        'min_names': min_names,
    }
    return min_data


def get_all_random_craft(actual_df):
    """
    Вычисляет среднее количество осколков на крафт одной
    игрушки случайной категории в случайной коллекции.
    """
    actual_albums_num = actual_df.shape[1]  # Количество выбранных альбомов
    toys_collected = actual_df.sum().sum()
    diff = (
        TOTAL_TOYS - (COLLECTIONS_NUM - actual_albums_num)
        * MAX_TOYS_IN_COLLECTION
    ) - toys_collected
    chance = diff/TOTAL_TOYS * 100
    # Среднее количество попыток на крафт
    average_attempts_num = 100 / chance
    # Среднее количество осколков на крафт
    average_fragments_num = (
        average_attempts_num * (ALL_RANDOM_CRAFT - ONE_TOY_FRAGMENTS)
    )
    data = {
        'chance': chance,
        'average_fragments_num': average_fragments_num,
    }
    return data


def get_specific_collection_craft(user_df, actual_albums):
    """
    Вычисляет среднее количество осколков на крафт одной
    игрушки в определенной коллекции в случайной категории.
    """
    # Осталось собрать игрушек для каждой коллекции
    missing_toys_in_collections = MAX_TOYS_IN_COLLECTION - user_df.sum()
    # Вероятность удачного крафта в каждой коллекции в случайной категории
    chance = missing_toys_in_collections / MAX_TOYS_IN_COLLECTION * 100
    # Среднее количество попыток на крафт в коллекции
    average_attempts_num = 100 / chance
    # Среднее количество осколков на крафт в определенной коллекции
    average_fragments_num = (
        average_attempts_num * (HALF_SPECIFIC_CRAFT - ONE_TOY_FRAGMENTS)
    )
    # Проверяем соответствие имен строк шансов и актуального датафрейма
    mask = ~chance.index.isin(actual_albums)
    # Заменяем значения строк, которые не актуальны
    mask = ~average_fragments_num.index.isin(actual_albums)
    average_fragments_num.loc[mask] = 'пропуск'
    # Минимальное количество осколков на крафт и коллекции соответственно
    min_data = get_min_data(average_fragments_num)
    data = {
        'chance': chance.to_dict(),
        'average_fragments_num': average_fragments_num.to_dict(),
    }
    return data, min_data


def get_specific_category_craft(actual_df, actual_albums):
    """
    Вычисляет среднее количество осколков на крафт одной игрушки
    в определенной категории в случайной коллекции.
    """
    # Осталось собрать игрушек для каждой категории
    missing_toys_in_categories = (
        full_df.sum(axis=1) / COLLECTIONS_NUM * len(actual_albums)
        - actual_df.sum(axis=1)
    )
    # Вероятность удачного крафта в каждой категории в случайной коллекции
    chance = missing_toys_in_categories / full_df.sum(axis=1) * 100
    # Среднее количество попыток на крафт в категории
    average_attempts_num = 100 / chance
    # Среднее количество осколков на крафт в определенной коллекции
    average_fragments_num = (
        average_attempts_num * (HALF_SPECIFIC_CRAFT - ONE_TOY_FRAGMENTS)
    )
    # Минимальное количество осколков на крафт и категории соответственно
    min_data = get_min_data(average_fragments_num)
    data = {
        'chance': chance.to_dict(),
        'average_fragments_num': average_fragments_num.to_dict(),
    }
    return data, min_data


def get_all_cpecific_craft(user_df, actual_albums):
    """
    Вычисляет среднее количество осколков на крафт одной игрушки
    в определенной категории в определенной коллекции.
    """
    # Осталось собрать игрушек для категории в каждой коллекции
    missing_toys = full_df - user_df
    # Вероятность удачного крафта в каждой категории каждой коллекции
    сhance = missing_toys / full_df * 100
    # Среднее количество попыток на крафт в определенной коллекции
    # и определенной категории
    average_attempts_num = 100 / сhance
    # Среднее количество осколков на крафт в определенной коллекции
    # и определенной категории
    average_fragments_num = (
        average_attempts_num * (ALL_SPECIFIC_CRAFT - ONE_TOY_FRAGMENTS)
    )
    # Заменяем значения в датафрейме, которые не актуальны
    average_fragments_num.loc[
        :, ~average_fragments_num.columns.isin(actual_albums)
    ] = 'пропуск'
    # Удаляем неактуальные столбцы, чтобы найти минимальные значения
    min_data = get_min_data(average_fragments_num, actual_albums)
    data = {
        'chance': сhance.to_dict(),
        'average_fragments_num': average_fragments_num.to_dict(),
    }
    return data, min_data


def main_calc(user_id):
    """
    Считает вероятности удачного крафта по колекциям
    и категориям и количество осколков, которое в среднем
    необходимо потратить на крафт игрушки. Возвращает
    результаты в виде словаря.
    """
    album = UserAlbums.objects.get(user_id=user_id)
    album_select = AlbumSelect.objects.get(user_id=user_id)
    user_df = get_user_df(album)  # Датафрейм пользователя
    # Датафрейм с актуальными альбомами
    actual_df, actual_albums = get_actual_df(user_df, album_select)
    all_random_craft = get_all_random_craft(actual_df)
    specific_collection_craft, collect_min = (
        get_specific_collection_craft(user_df, actual_albums)
    )
    specific_category_craft, category_min = (
        get_specific_category_craft(actual_df, actual_albums)
    )
    all_specific_craft, all_min = get_all_cpecific_craft(
        user_df, actual_albums
    )
    tables_data = {
        'all_random_craft': all_random_craft,
        'specific_collection_craft': specific_collection_craft,
        'specific_category_craft': specific_category_craft,
        'all_specific_craft': all_specific_craft,
    }
    min_data = {
        'all_random_min': all_random_craft['average_fragments_num'],
        'collect_min': collect_min,
        'category_min': category_min,
        'all_min': all_min,
    }
    return tables_data, min_data
