from django import forms
from .models import UserAlbums


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
    hanging = forms.PositiveSmallIntegerField(
        help_text=helps['hanging_text'],
    )
    crown = forms.PositiveSmallIntegerField(
        help_text=helps['crown_text'],
    )
    gift = forms.PositiveSmallIntegerField(
        help_text=helps['gift_text'],
    )
    garland = forms.PositiveSmallIntegerField(
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
        labels = {
            'hanging': 'national_hanging',
            'crown': 'national_crown',
            'gift': 'national_gift',
            'garland': 'national_garland'
        }


class EasternForm(forms.Form):
    """
    Форма для записи восточного альбома игрушек.
    """
    hanging = forms.PositiveSmallIntegerField(
        help_text=helps['hanging_text'],
    ),
    crown = forms.PositiveSmallIntegerField(
        help_text=helps['crown_text'],
    ),
    gift = forms.PositiveSmallIntegerField(
        help_text=helps['gift_text'],
    ),
    garland = forms.PositiveSmallIntegerField(
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
    labels = {
        'hanging': 'eastern_hanging',
        'crown': 'eastern_crown',
        'gift': 'eastern_gift',
        'garland': 'eastern_garland'
    }


class MagicForm(forms.Form):
    """
    Форма для записи сказочного альбома игрушек.
    """
    hanging = forms.PositiveSmallIntegerField(
        help_text=helps['hanging_text'],
    ),
    crown = forms.PositiveSmallIntegerField(
        help_text=helps['crown_text'],
    ),
    gift = forms.PositiveSmallIntegerField(
        help_text=helps['gift_text'],
    ),
    garland = forms.PositiveSmallIntegerField(
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
    labels = {
        'hanging': 'magic_hanging',
        'crown': 'magic_crown',
        'gift': 'magic_gift',
        'garland': 'magic_garland'
    }


class ChristmasForm(forms.Form):
    """
    Форма для записи Рождественского альбома.
    """
    hanging = forms.PositiveSmallIntegerField(
        help_text=helps['hanging_text'],
    ),
    crown = forms.PositiveSmallIntegerField(
        help_text=helps['crown_text'],
    ),
    gift = forms.PositiveSmallIntegerField(
        help_text=helps['gift_text'],
    ),
    garland = forms.PositiveSmallIntegerField(
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
    labels = {
        'hanging': 'christmas_hanging',
        'crown': 'christmas_crown',
        'gift': 'christmas_gift',
        'garland': 'christmas_garland'
    }
