from .initial_data import INITIAL_DATA
from .mongo_init import toys


def add_new_user_collection(username):
    """Добавляет пустую коллекцию игрушек при регистрации
    новых пользователей."""

    user_data = toys.find_one({'username': username})
    if user_data is None:
        print(f'Добавляем коллекцию для пользователя {username}')
        toys.insert_one({
            'username': username,
            'collection': INITIAL_DATA
        })
    else:
        pass
        # Если пользователь был зарегистрирован раньше, но был удален
        # а теперь опять создается пользователь с таким именем, то обнуляем
        # его коллекцию игрушек
        # toys.update_one(
        #     {'username': username},
        #     {'$set': {'collection': INITIAL_DATA}}
        # )


def main():
    pass


if __name__ == '__main__':
    main()
