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
        validators=[MaxValueValidator(MAX_HANGING)]
    )
    national_crown = models.PositiveSmallIntegerField(
        verbose_name='Отечественный-навершие',
        validators=[MaxValueValidator(MAX_CROWN)]
    )
    national_gift = models.PositiveSmallIntegerField(
        verbose_name='Отечественный-подарки',
        validators=[MaxValueValidator(MAX_GIFT)]
    ),
    national_garland = models.PositiveSmallIntegerField(
        verbose_name='Отечественный-гирлянды',
        validators=[MaxValueValidator(MAX_GARLAND)]
    ),
    eastern_hanging = models.PositiveSmallIntegerField(
        verbose_name='Восточный-подвесные',
        validators=[MaxValueValidator(MAX_HANGING)]
    ),
    eastern_crown = models.PositiveSmallIntegerField(
        verbose_name='Восточный-навершие',
        validators=[MaxValueValidator(MAX_CROWN)]
    ),
    eastern_gift = models.PositiveSmallIntegerField(
        verbose_name='Восточный-подарки',
        validators=[MaxValueValidator(MAX_GIFT)]
    ),
    eastern_garland = models.PositiveSmallIntegerField(
        verbose_name='Восточный-гирлянды',
        validators=[MaxValueValidator(MAX_GARLAND)]
    ),
    magic_hanging = models.PositiveSmallIntegerField(
        verbose_name='Сказочный-подвесные',
        validators=[MaxValueValidator(MAX_HANGING)]
    ),
    magic_crown = models.PositiveSmallIntegerField(
        verbose_name='Сказочный-навершие',
        validators=[MaxValueValidator(MAX_CROWN)]
    ),
    magic_gift = models.PositiveSmallIntegerField(
        verbose_name='Сказочный-подарки',
        validators=[MaxValueValidator(MAX_GIFT)]
    ),
    magic_garland = models.PositiveSmallIntegerField(
        verbose_name='Сказочный-гирлянды',
        validators=[MaxValueValidator(MAX_GARLAND)]
    ),
    christmas_hanging = models.PositiveSmallIntegerField(
        verbose_name='Рождественский-подвесные',
        validators=[MaxValueValidator(MAX_HANGING)]
    ),
    christmas_crown = models.PositiveSmallIntegerField(
        verbose_name='Рождественский-навершие',
        validators=[MaxValueValidator(MAX_CROWN)]
    ),
    christmas_gift = models.PositiveSmallIntegerField(
        verbose_name='Рождественский-подарки',
        validators=[MaxValueValidator(MAX_GIFT)]
    ),
    christmas_garland = models.PositiveSmallIntegerField(
        verbose_name='Рождественский-гирлянды',
        validators=[MaxValueValidator(MAX_GARLAND)]
    ),
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Время обновления',
    )
