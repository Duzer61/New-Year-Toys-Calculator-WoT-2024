from django.core.validators import MaxValueValidator
from django.db import models
from users.models import User

from .constants import MAX_CROWN, MAX_GARLAND, MAX_GIFT, MAX_HANGING


class UserAlbums(models.Model):
    """
    Модель для хранения пользовательских альбомов.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='albums',
        verbose_name='Пользователь',
    )
    national_hanging = models.PositiveSmallIntegerField(
        verbose_name='Отечественный-подвесные',
        validators=[MaxValueValidator(MAX_HANGING)],
        default=0
    )
    national_crown = models.PositiveSmallIntegerField(
        verbose_name='Отечественный-навершие',
        validators=[MaxValueValidator(MAX_CROWN)],
        default=0
    )
    national_gift = models.PositiveSmallIntegerField(
        verbose_name='Отечественный-подарки',
        validators=[MaxValueValidator(MAX_GIFT)],
        default=0
    )
    national_garland = models.PositiveSmallIntegerField(
        verbose_name='Отечественный-гирлянды',
        validators=[MaxValueValidator(MAX_GARLAND)],
        default=0
    )
    eastern_hanging = models.PositiveSmallIntegerField(
        verbose_name='Восточный-подвесные',
        validators=[MaxValueValidator(MAX_HANGING)],
        default=0
    )
    eastern_crown = models.PositiveSmallIntegerField(
        verbose_name='Восточный-навершие',
        validators=[MaxValueValidator(MAX_CROWN)],
        default=0
    )
    eastern_gift = models.PositiveSmallIntegerField(
        verbose_name='Восточный-подарки',
        validators=[MaxValueValidator(MAX_GIFT)],
        default=0
    )
    eastern_garland = models.PositiveSmallIntegerField(
        verbose_name='Восточный-гирлянды',
        validators=[MaxValueValidator(MAX_GARLAND)],
        default=0
    )
    magic_hanging = models.PositiveSmallIntegerField(
        verbose_name='Сказочный-подвесные',
        validators=[MaxValueValidator(MAX_HANGING)],
        default=0
    )
    magic_crown = models.PositiveSmallIntegerField(
        verbose_name='Сказочный-навершие',
        validators=[MaxValueValidator(MAX_CROWN)],
        default=0
    )
    magic_gift = models.PositiveSmallIntegerField(
        verbose_name='Сказочный-подарки',
        validators=[MaxValueValidator(MAX_GIFT)],
        default=0
    )
    magic_garland = models.PositiveSmallIntegerField(
        verbose_name='Сказочный-гирлянды',
        validators=[MaxValueValidator(MAX_GARLAND)],
        default=0
    )
    christmas_hanging = models.PositiveSmallIntegerField(
        verbose_name='Рождественский-подвесные',
        validators=[MaxValueValidator(MAX_HANGING)],
        default=0
    )
    christmas_crown = models.PositiveSmallIntegerField(
        verbose_name='Рождественский-навершие',
        validators=[MaxValueValidator(MAX_CROWN)],
        default=0
    )
    christmas_gift = models.PositiveSmallIntegerField(
        verbose_name='Рождественский-подарки',
        validators=[MaxValueValidator(MAX_GIFT)],
        default=0
    )
    christmas_garland = models.PositiveSmallIntegerField(
        verbose_name='Рождественский-гирлянды',
        validators=[MaxValueValidator(MAX_GARLAND)],
        default=0
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Время обновления',
    )

    class Meta:
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'
        ordering = ('-created_at',)

    def __str__(self):
        return self.user.username
