from django import forms
from .models import UserAlbums
from .constants import MAX_CROWN, MAX_GARLAND, MAX_GIFT, MAX_HANGING


# class ToysForm(forms.Form):
#     hanging = forms.IntegerField(min_value=0, max_value=MAX_HANGING)
#     crown = forms.IntegerField(min_value=0, max_value=MAX_CROWN)
#     gift = forms.IntegerField(min_value=0, max_value=MAX_GIFT)
#     garland = forms.IntegerField(min_value=0, max_value=MAX_GARLAND)
helps = {
    'hanging_text': "Количество подвесных игрушек",
    'crown_text': "Количество наверший",
    'gift_text': "Количество подарков",
    'garland_text': "Количество гирлянд",
}


class NationalForm(forms.Form):
    """
    Форма для записи альбома отечественных игрушек.
    """
    national_hanging = forms.PositiveSmallIntegerField(
        help_text=helps['hanging_text'],
    )
    national_crown = forms.PositiveSmallIntegerField(
        help_text=helps['crown_text'],
    )
    national_gift = forms.PositiveSmallIntegerField(
        help_text=helps['gift_text'],
    )
    national_garland = forms.PositiveSmallIntegerField(
        help_text=helps['garland_text'],
    )

    class Meta:
        model = UserAlbums
        fields = [
            'national_hanging',
            'national_crown',
            'national_gift',
            'national_garland'
        ]


class EasternForm(forms.Form):
    """
    Форма для записи восточного альбома игрушек.
    """
    eastern_hanging = forms.PositiveSmallIntegerField(
        help_text=helps['hanging_text'],
    ),
    eastern_crown = forms.PositiveSmallIntegerField(
        help_text=helps['crown_text'],
    ),
    eastern_gift = forms.PositiveSmallIntegerField(
        help_text=helps['gift_text'],
    ),
    eastern_garland = forms.PositiveSmallIntegerField(
        help_text=helps['garland_text'],
    )

    class Meta:
        model = UserAlbums
        fields = [
            'eastern_hanging',
            'eastern_crown',
            'eastern_gift',
            'eastern_garland'
        ]


class MagicForm(forms.Form):
    """
    Форма для записи сказочного альбома игрушек.
    """
    magic_hanging = forms.PositiveSmallIntegerField(
        help_text=helps['hanging_text'],
    ),
    magic_crown = forms.PositiveSmallIntegerField(
        help_text=helps['crown_text'],
    ),
    magic_gift = forms.PositiveSmallIntegerField(
        help_text=helps['gift_text'],
    ),
    magic_garland = forms.PositiveSmallIntegerField(
        help_text=helps['garland_text'],
    )

    class Meta:
        model = UserAlbums
        fields = [
            'magic_hanging',
            'magic_crown',
            'magic_gift',
            'magic_garland'
        ]


class ChristmasForm(forms.Form):
    """
    Форма для записи Рождественского альбома.
    """
    christmas_hanging = forms.PositiveSmallIntegerField(
        help_text=helps['hanging_text'],
    ),
    christmas_crown = forms.PositiveSmallIntegerField(
        help_text=helps['crown_text'],
    ),
    christmas_gift = forms.PositiveSmallIntegerField(
        help_text=helps['gift_text'],
    ),
    christmas_garland = forms.PositiveSmallIntegerField(
        help_text=helps['garland_text'],
    )

    class Meta:
        model = UserAlbums
        fields = [
            'christmas_hanging',
            'christmas_crown',
            'christmas_gift',
            'christmas_garland'
        ]
