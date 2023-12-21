from django.db import models
from users.models import User


class AlbumSelect(models.Model):
    """
    Модель для хранения настроек пользователя по выбору альбомов,
    которые он планирует собрать.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='selects',
        verbose_name='Пользователь',
    )
    national = models.BooleanField(
        default=True,
        verbose_name='Отечественный'
    )
    eastern = models.BooleanField(
        default=True,
        verbose_name='Восточный'
    )
    magic = models.BooleanField(
        default=True,
        verbose_name='Сказочный'
    )
    christmas = models.BooleanField(
        default=True,
        verbose_name='Рождество'
    )
