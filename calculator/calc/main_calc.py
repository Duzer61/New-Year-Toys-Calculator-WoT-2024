import pandas as pd

from .constants import (ALL_RANDOM_CRAFT, HALF_SPECIFIC_CRAFT, MAX_CROWN,
                        MAX_GARLAND, MAX_GIFT, MAX_HANGING,
                        MAX_TOYS_IN_COLLECTION, ONE_TOY_FRAGMENTS, TOTAL_TOYS)
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
    return f'Среднее количество осколков: {round(average_fragments_num, 2)}'


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
    return (
        f'Среднее количество осколков на крафт в определенной коллекции: \n'
        f'{round(average_fragments_num, 2)}'
    )


def trial_function(username):
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

        return specific_collection_craft
