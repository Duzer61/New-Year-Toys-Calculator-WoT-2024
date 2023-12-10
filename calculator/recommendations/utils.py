import numpy as np
from calc.constants import ANTIPOVTORITEL_CRAFT

UNCERT_COEF = 0.7  # Коэффициент неопределенности. Обозначает при какой разнице
# значений можно рассмотреть и другой вариант

# Заготовки названий для рекомендаций
titles_translation = {
    'national': 'Отечественная',
    'eastern': 'Восточная',
    'magic': 'Сказочная',
    'christmas': 'Рождественская',
    'hanging': 'Подвесная',
    'crown': 'Навершие',
    'gift': 'Подарок',
    'garland': 'Гирлянда',
}

# Заготовки сообщений для рекомендаций
anti_povtoritel_definitely = 'Однозначно пора использовать антиповторитель!'
anti_povtoritel_maybe = (
    'Чисто математически еще рано использовать антиповторитель. '
    'Но, кажется уже лучше подстраховаться и крафтить с ним.'
)
congratulations = 'Все коллекции 5 лвл. собраны. Поздравляю!'
all_random_definitely = (
    'Выгоднее крафтить в случайной коллекции и случайной категории. '
    'Это может занять больше попыток, но все-равно ожидаемая трата '
    'осколков будет меньше. Не забывайте разбивать ненужные игрушки.'
)
all_random_maybe = (
    'Чисто математически выгоднее крафтить в случайной коллекции и случайной '
    'категории. Это может занять больше попыток, но все-равно ожидаемая трата '
    'осколков меньше. Как вариант, можно воспользоваться советом ниже. '
    'Может потратится больше осколков, но попыток будет меньше.'
)
collect_definitely = "Выгоднее крафтить в коллекциях: "
collect_maybe = "Можно также крафтить в коллекциях: "
category_definitely = "Выгоднее крафтить в категориях: "
category_maybe = "Можно также крафтить в категориях: "


def anti_povtoritel_check(value):
    """Проверяет на крафт с антиповторителем."""

    message = ''
    if np.isinf(value):
        message = congratulations
    elif value >= ANTIPOVTORITEL_CRAFT:
        message = anti_povtoritel_definitely
    elif value >= ANTIPOVTORITEL_CRAFT * UNCERT_COEF:
        message = anti_povtoritel_maybe
    return message


def all_random_check(name, value, value_2):
    """Проверяет на целесообразность полностью случайного крафта."""

    is_definitely = False  # Флаг, на однозначную целесообразность
    if name == 'all_random_min' and value_2 * UNCERT_COEF <= value:
        message = all_random_maybe
    elif name == 'all_random_min':
        message = all_random_definitely
        is_definitely = True
    else:
        message = ''
        is_definitely = True
    return message, is_definitely


def collect_check(name, name_2, value, value_2, is_definitely, min_data):
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


def get_advice(min_data):
    """Возвращает рекомендации по крафту."""

    print(f'min_data: {min_data}')  # для отладки, удалить позже. min_data: {min_data)
    # минимальные значения осколков по разным способам крафта
    min_values = {
        'all_random_min': min_data['all_random_min'],
        'collect_min': min_data['collect_min']['min_value'],
        'category_min': min_data['category_min']['min_value'],
        'all_min': min_data['all_min']['min_value'],
    }
    min_values = sorted(min_values.items(), key=lambda x: x[1])
    print(f'min_values: {min_values}')
    min_name, min_value = min_values[0][0], min_values[0][1]
    min_name_2, min_value_2 = min_values[1][0], min_values[1][1]
    min_name_3, min_value_3 = min_values[2][0], min_values[2][1]
    rec_message = ''  # сообщение с рекомендацией крафта
    message = anti_povtoritel_check(min_value)
    message_2 = ''
    if message:  # если есть рекомендации с анитповторителем, то возвращаем их
        return message, message_2
    message, is_definitely = all_random_check(min_name, min_value, min_value_2)
    if message and is_definitely:
        return message, message_2
    message_2 = collect_check(
        min_name, min_name_2, min_value, min_value_2, is_definitely, min_data
    )
    if not message_2:
        message_2 = 'Пока не накодил...'
    return message, message_2
