import numpy as np
from calc.constants import ANTIPOVTORITEL_CRAFT

# Заготовки сообщений для рекомендаций
anti_povtoritel_definitely = 'Однозначно пора использовать антиповторитель!'
anti_povtoritel_maybe = (
    'Чисто математически еще рано использовать антиповторитель. '
    'Но, кажется уже лучше подстраховаться и крафтить с ним.'
)
congratulations = 'Все коллекции 5 лвл. собраны. Поздравляю!'


def anti_povtoritel_check(value):
    """Проверяет на крафт с антиповторителем."""

    message = ''
    if np.isinf(value):
        message = congratulations
    elif value >= ANTIPOVTORITEL_CRAFT:
        message = anti_povtoritel_definitely
    elif value >= ANTIPOVTORITEL_CRAFT * 0.75:
        message = anti_povtoritel_maybe
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
    if not message:
        print('Рекомендации нет')
    else:
        print(message)
