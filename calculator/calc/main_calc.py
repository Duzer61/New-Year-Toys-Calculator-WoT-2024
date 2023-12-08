import pandas as pd

from .constants import (ALL_RANDOM_CRAFT, ALL_SPECIFIC_CRAFT,
                        HALF_SPECIFIC_CRAFT, MAX_CROWN, MAX_GARLAND, MAX_GIFT,
                        MAX_HANGING, MAX_TOYS_IN_COLLECTION, ONE_TOY_FRAGMENTS,
                        TOTAL_TOYS)
from .utils import toys

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


def get_user_collection(username):
    """Извлекает из бд и возвращает коллекции пользователя."""
    user_collection = toys.find_one(
        {'username': username},
    )['collection']
    return user_collection


def get_all_random_craft(user_df):
    """
    Вычисляет среднее количество осколков на крафт одной
    игрушки случайной категории в случайной коллекции.
    """

    toys_collected = user_df.sum().sum()  # Количество собранных игрушек
    diff = TOTAL_TOYS - toys_collected  # Всего осталось собрать игрушек
    print(f'Всего осталось собрать {diff} игрушек.')
    chance = diff/TOTAL_TOYS * 100
    print(f'Вероятность удачного крафта одной игрушки: {round(chance, 2)}')
    average_attempts_num = 100 / chance
    print(f'Среднее количество попыток: {round(average_attempts_num, 2)}')
    average_fragments_num = (
        (average_attempts_num - 1) * (ALL_RANDOM_CRAFT - ONE_TOY_FRAGMENTS)
        + ALL_RANDOM_CRAFT
    )
    print(
        f'Среднее количество осколков на случайный крафт: '
        f'{round(average_fragments_num, 2)}'
    )
    return 'Далее вычисляем по коллекциям.'


def get_specific_collection_craft(user_df):
    """
    Вычисляет среднее количество осколков на крафт одной
    игрушки в определенной коллекции в случайной катекории.
    """
    # Осталось собрать игрушек для каждой коллекции
    missing_toys_in_collections = MAX_TOYS_IN_COLLECTION - user_df.sum()
    print(f'Осталось собрать: \n{missing_toys_in_collections}')
    # Вероятность удачного крафта в каждой коллекции в случайной категории
    chance = missing_toys_in_collections / MAX_TOYS_IN_COLLECTION * 100
    print(
        f'Вероятность удачного крафта в определенной коллекции: \n'
        f'{round(chance, 2)}'
    )
    # Среднее количество попыток на крафт в коллекции
    average_attempts_num = 100 / chance
    print(
        f'Среднее количество попыток на крафт в определенной коллекции: \n'
        f'{round(average_attempts_num, 2)}'
    )
    # Среднее количество осколков на крафт в определенной коллекции
    average_fragments_num = (
        (average_attempts_num - 1) * (HALF_SPECIFIC_CRAFT - ONE_TOY_FRAGMENTS)
        + HALF_SPECIFIC_CRAFT
    )
    print(
        f'Среднее количество осколков на крафт в определенной коллекции: \n'
        f'{round(average_fragments_num, 2)}'
    )
    return 'Далее вычисляем по категориям...'


def get_specific_category_craft(user_df):
    """
    Вычисляет среднее количество осколков на крафт одной игрушки
    в определенной категории в случайной коллекции.
    """
    # Осталось собрать игрушек для каждой категории
    missing_toys_in_categories = full_df.sum(axis=1) - user_df.sum(axis=1)
    print(missing_toys_in_categories)
    # Вероятность удачного крафта в каждой категории в случайной коллекции
    chance = missing_toys_in_categories / full_df.sum(axis=1) * 100
    print(
        f'Вероятность удачного крафта в определенной категории: \n'
        f'{round(chance, 2)}'
    )
    # Среднее количество попыток на крафт в категории
    average_attempts_num = 100 / chance
    print(
        f'Среднее количество попыток на крафт в определенной категории: \n'
        f'{round(average_attempts_num, 2)}'
    )
    # Среднее количество осколков на крафт в определенной коллекции
    average_fragments_num = (
        (average_attempts_num - 1) * (HALF_SPECIFIC_CRAFT - ONE_TOY_FRAGMENTS)
        + HALF_SPECIFIC_CRAFT
    )
    print(
        f'Среднее количество осколков на крафт в определенной категории: \n'
        f'{round(average_fragments_num, 2)}'
    )
    return 'Далее...'


def get_all_cpecific_craft(user_df):
    """
    Вычисляет среднее количество осколков на крафт одной игрушки
    в определенной категории в определенной коллекции.
    """
    # Осталось собрать игрушек для категории в каждой коллекции
    missing_toys = full_df - user_df
    print(missing_toys)
    # Вероятность удачного крафта в каждой категории каждой коллекции
    сhance = missing_toys / full_df * 100
    print(
        f'Вероятность удачного крафта в каждой категории каждой коллекции: \n'
        f'{round(сhance, 2)}'
    )
    # Среднее количество попыток на крафт в определенной коллекции
    # и определенной категории
    average_attempts_num = 100 / сhance
    print(
        f'Среднее количество попыток на крафт в определенной коллекции '
        f'и определенной категории: \n {round(average_attempts_num, 2)}'
    )
    # Среднее количество осколков на крафт в определенной коллекции
    # и определенной категории
    average_fragments_num = (
        (average_attempts_num - 1) * (ALL_SPECIFIC_CRAFT - ONE_TOY_FRAGMENTS)
        + ALL_SPECIFIC_CRAFT
    )
    print(
        f'Среднее количество осколков на крафт в определенной коллекции '
        f'и определенной категории: \n {round(average_fragments_num, 2)}'
    )
    return average_fragments_num


def main_calc(username):
    """Функция для проверки работы калькулятора."""
    print('Зашли в калькулятор')
    user_collection = get_user_collection(username)
    if user_collection:
        print(user_collection)
        user_df = pd.DataFrame(user_collection)
        print(user_df)
        print(f'Всего собрано {user_df.sum().sum()} игрушек')
        print(full_df)
        print(user_df == full_df)
        if (user_df == full_df).all().all():
            return 'Все коллекции собраны'
        all_random_craft = get_all_random_craft(user_df)
        print(all_random_craft)
        specific_collection_craft = get_specific_collection_craft(user_df)
        print(specific_collection_craft)
        specific_category_craft = get_specific_category_craft(user_df)
        print(specific_category_craft)
        all_specific_craft = get_all_cpecific_craft(user_df)
        return all_specific_craft
