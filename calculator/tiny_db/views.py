from tinydb import Query

from .database import table
from .initial_data import initial_data


def add_new_user_collection(username):
    """Добавляет пустую коллекцию игрушек при регистрации
    новых пользователей."""

    user_data = table.get(Query().username == username)
    if user_data is None:
        print(f'Добавляем коллекцию для пользователя {username}')
        table.insert(
            {
                'username': username,
                'collection': initial_data
            }
        )
    else:
        # Если пользователь был зарегистрирован раньше, но был удален
        # а теперь опять создается пользователь с таким именем, то обнуляем
        # его коллекцию игрушек
        print(f'Обнуляем коллекцию для пользователя {username}')
        table.update(
            {'collection': initial_data}, Query().username == username
        )


def main():
    pass


if __name__ == '__main__':
    main()
