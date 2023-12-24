import numpy as np
from calc.constants import (ALL_SPECIFIC_CRAFT, ANTIPOVTORITEL_CRAFT,
                            HALF_SPECIFIC_CRAFT, ONE_TOY_FRAGMENTS,
                            UNCERT_COEF)

from .message_blanks import (all_random_better_next, all_random_definitely,
                             all_random_maybe, anti_povtoritel_definitely,
                             anti_povtoritel_maybe, category_definitely,
                             category_maybe, collect_category,
                             collect_definitely, collect_maybe,
                             congratulations, titles_translation)


def anti_povtoritel_check(value):
    """Проверяет на крафт с антиповторителем."""

    message = ''
    if np.isinf(value):
        message = congratulations
    elif value >= (ANTIPOVTORITEL_CRAFT - ONE_TOY_FRAGMENTS):
        message = anti_povtoritel_definitely
    elif value >= (ANTIPOVTORITEL_CRAFT - ONE_TOY_FRAGMENTS) * UNCERT_COEF:
        message = anti_povtoritel_maybe
    return message


def all_random_check(name, name_2, value, value_2):
    """Проверяет на целесообразность полностью случайного крафта."""

    is_definitely = False  # Флаг, на однозначную целесообразность
    # если совет может быть неоднозначный
    if name == 'all_random_min' and (
        (value_2 - ONE_TOY_FRAGMENTS) * UNCERT_COEF
        <= (value - ONE_TOY_FRAGMENTS)
    ):
        # и при этом если следующий по выгодности крафт будет
        # со 100% вероятностью
        if name_2 == 'all_min' and value_2 == (
            ALL_SPECIFIC_CRAFT - ONE_TOY_FRAGMENTS
        ):
            message = all_random_better_next
        elif (
            (name_2 == 'category_min' or name_2 == 'collect_min')
            and value_2 == (HALF_SPECIFIC_CRAFT - ONE_TOY_FRAGMENTS)
        ):
            message = all_random_better_next
        else:
            message = all_random_maybe
    elif name == 'all_random_min':
        message = all_random_definitely
        is_definitely = True
    else:
        message = ''
        is_definitely = True
    return message, is_definitely


def collect_category_check(name, name_2, is_definitely, min_data):
    """Проверяет на целесообразность крафта в коллекции."""

    message = ''
    if is_definitely:  # Если предыдущая проверка однозначно не прошла.
        if name == 'collect_min':
            message = collect_definitely + (
                f"{', '.join(
                    titles_translation[title]for title in
                    min_data['collect_min']['min_names']
                )}"
            )
        elif name == 'category_min':
            message = category_definitely + (
                f"{', '.join(
                    titles_translation[title]for title in
                    min_data['category_min']['min_names']
                )}"
            )
    else:
        if name_2 == 'collect_min':
            message = collect_maybe + (
                f"{', '.join(
                    titles_translation[title]for title in
                    min_data['collect_min']['min_names']
                )}"
            )
        elif name_2 == 'category_min':
            message = category_maybe + (
                f"{', '.join(
                    titles_translation[title]for title in
                    min_data['category_min']['min_names']
                )}"
            )
    return message


def all_check(name, name_2, min_data):
    """
    Проверяет на целесообразность крафта в определенной коллекции
    и определенной категории.
    """
    message = ''
    if name == 'all_min' or name_2 == 'all_min':
        message = collect_category
        min_names = min_data['all_min']['min_names']
        for i, titles in enumerate(min_names):
            extra_message = (
                f"{' - '.join(titles_translation[title]for title in titles)}"
            )
            message += extra_message
            if i < len(min_names) - 1:
                message += ', '
    return message


def get_advice(min_data):
    """Возвращает рекомендации по крафту."""

    # минимальные значения осколков по разным способам крафта
    min_values = {
        'all_random_min': min_data['all_random_min'],
        'collect_min': min_data['collect_min']['min_value'],
        'category_min': min_data['category_min']['min_value'],
        'all_min': min_data['all_min']['min_value'],
    }
    min_values = sorted(min_values.items(), key=lambda x: x[1])
    print(f'min_values:\n{min_values}')
    min_name, min_value = min_values[0][0], min_values[0][1]
    min_name_2, min_value_2 = min_values[1][0], min_values[1][1]
    print(f'min_name: {min_name}, min_value: {min_value}')
    print(f'min_name_2: {min_name_2}, min_value_2: {min_value_2}')
    message = anti_povtoritel_check(min_value)
    message_2 = ''
    if message:  # если есть рекомендации с анитповторителем, то возвращаем их
        return message, message_2
    message, is_definitely = all_random_check(
        min_name, min_name_2, min_value, min_value_2
    )
    if message and is_definitely:  # если есть однозначная рекомендация
        return message, message_2
    message_2 = collect_category_check(  # дополнительный совет
        min_name, min_name_2, is_definitely, min_data
    )
    if message_2:
        return message, message_2

    message_2 = all_check(min_name, min_name_2, min_data)
    return message, message_2
