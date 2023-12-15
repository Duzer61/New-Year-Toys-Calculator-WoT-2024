from django import forms
from .models import UserAlbums


class NationalForm(forms.ModelForm):
    """
    Форма для записи альбома отечественных игрушек.
    """

    class Meta:
        model = UserAlbums
        fields = [
            'national_hanging',
            'national_crown',
            'national_gift',
            'national_garland'
        ]


class EasternForm(forms.ModelForm):
    """
    Форма для записи восточного альбома игрушек.
    """
    class Meta:
        model = UserAlbums
        fields = [
            'eastern_hanging',
            'eastern_crown',
            'eastern_gift',
            'eastern_garland'
        ]


class MagicForm(forms.ModelForm):
    """
    Форма для записи сказочного альбома игрушек.
    """

    class Meta:
        model = UserAlbums
        fields = [
            'magic_hanging',
            'magic_crown',
            'magic_gift',
            'magic_garland'
        ]


class ChristmasForm(forms.ModelForm):
    """
    Форма для записи Рождественского альбома.
    """

    class Meta:
        model = UserAlbums
        fields = [
            'christmas_hanging',
            'christmas_crown',
            'christmas_gift',
            'christmas_garland'
        ]
