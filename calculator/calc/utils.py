from mongodb.initial_data import COLLECTION_DATA
from mongodb.mongo_init import results, toys
from mongodb.views import add_new_user_collection
from recommendations.utils import get_advice

from .main_calc import main_calc


def save_user_result(username, result):
    """Сохраняет данные о рассчетах пользователя."""

    results.update_one(
        {'username': username},
        {'$set': {'result': result}},
        upsert=True
    )


def form_handler(request, form, username, collection_name):
    """Обрабатывает форму."""

    is_calc = False  # Флаг, если производился рассчет
    collection_full_name = 'collection.' + collection_name
    if form.is_valid():
        forms_data = form.cleaned_data
        toys.update_one(
            {'username': username},
            {'$set': {collection_full_name: forms_data}}
        )
        if 'calculate' in request.POST:  # Если нажата кнопка "Рассчитать"
            tables_data, min_data = main_calc(username)
            # print(tables_data)
            advice = get_advice(min_data)
            save_user_result(username, tables_data)
            is_calc = True
    user_data = toys.find_one(
        {'username': username},
        {collection_full_name: 1}
    )
    # Проверка, если пользователь был создан, но не была создана коллекция
    if user_data:
        user_data = user_data['collection'][collection_name]
    else:  # Если у пользователя нет коллекции, то создаем пустую
        add_new_user_collection(username)
        user_data = COLLECTION_DATA
    return user_data, is_calc
