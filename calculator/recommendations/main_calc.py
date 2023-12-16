import pandas as pd
from calc.constants import (ALL_RANDOM_CRAFT, ALL_SPECIFIC_CRAFT,
                            HALF_SPECIFIC_CRAFT, MAX_CROWN, MAX_GARLAND,
                            MAX_GIFT, MAX_HANGING, MAX_TOYS_IN_COLLECTION,
                            ONE_TOY_FRAGMENTS, TOTAL_TOYS)
from calc.models import UserAlbums

FULL_COLLECTION_DATA = {
    'hanging': MAX_HANGING,
    'crown': MAX_CROWN,
    'gift': MAX_GIFT,
    'garland': MAX_GARLAND
}

full_df = pd.DataFrame(
    {
        'national': FULL_COLLECTION_DATA,
        'eastern': FULL_COLLECTION_DATA,
        'magic': FULL_COLLECTION_DATA,
        'christmas': FULL_COLLECTION_DATA,
    }
)


def get_user_df(album):
    """
    Возвращает DataFrame pandas для коллекции пользователя.
    """

    albums = ['national', 'eastern', 'magic', 'christmas']
    items = ['hanging', 'crown', 'gift', 'garland']
    album_data = {}
    for album_type in albums:
        album_data[album_type] = {}
        for item in items:
            element_name = f'{album_type}_{item}'
            album_data[album_type][item] = getattr(album, element_name)
    user_df = pd.DataFrame(album_data)
    return user_df


def get_min_data(average_fragments_num):
    """
    Возвращает значение минимального количества осколков на крафт
    по коллекциям или по категориям, а так-же имена коллекций или
    категорий с этим значением.
    """
    min_value = average_fragments_num.min()
    min_names = average_fragments_num[
        average_fragments_num == min_value
    ].index.to_list()
    min_data = {
        'min_value': min_value,
        'min_names': min_names,
    }
    return min_data


def get_all_random_craft(user_df):
    """
    Вычисляет среднее количество осколков на крафт одной
    игрушки случайной категории в случайной коллекции.
    """

    toys_collected = user_df.sum().sum()  # Количество собранных игрушек
    diff = TOTAL_TOYS - toys_collected  # Всего осталось собрать игрушек
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


def get_specific_collection_craft(user_df):
    """
    Вычисляет среднее количество осколков на крафт одной
    игрушки в определенной коллекции в случайной катекории.
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
    # Минимальное количество осколков на крафт и коллекции соответственно
    min_data = get_min_data(average_fragments_num)
    data = {
        'chance': chance.to_dict(),
        'average_fragments_num': average_fragments_num.to_dict(),
    }
    return data, min_data


def get_specific_category_craft(user_df):
    """
    Вычисляет среднее количество осколков на крафт одной игрушки
    в определенной категории в случайной коллекции.
    """
    # Осталось собрать игрушек для каждой категории
    missing_toys_in_categories = full_df.sum(axis=1) - user_df.sum(axis=1)
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


def get_all_cpecific_craft(user_df):
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
    # Минимальное количество осколков на крафт и
    # коллекции-категории соответственно
    min_value = average_fragments_num.min().min()
    min_names = average_fragments_num[
        average_fragments_num == min_value
    ].stack().index.tolist()
    min_data = {
        'min_value': min_value,
        'min_names': min_names,
    }
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
    user_df = get_user_df(album)
    print(f'user_df: \n{user_df}')

    all_random_craft = get_all_random_craft(user_df)
    specific_collection_craft, collect_min = (
        get_specific_collection_craft(user_df)
    )
    specific_category_craft, category_min = (
        get_specific_category_craft(user_df)
    )
    all_specific_craft, all_min = get_all_cpecific_craft(user_df)
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
