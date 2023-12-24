from django.db import models
from users.models import User
from django.core.exceptions import ValidationError


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
    toggle = models.BooleanField(
        default=False,
        verbose_name='Переключатель',
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

    def clean(self):
        """
        Не позволят удалить все альбомы из расчета.
        Хотя бы один должен быть включен.
        """
        toggle = self.toggle
        if not toggle:
            self.toggle = False
            self.national = True
            self.eastern = True
            self.magic = True
            self.christmas = True
        if not any([self.national, self.eastern, self.magic, self.christmas]):
            raise ValidationError('Должен остаться хотя-бы один :)')
