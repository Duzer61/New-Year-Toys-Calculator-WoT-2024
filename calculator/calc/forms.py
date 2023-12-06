from django import forms

# Максимальные количество игрушек в каждой категории
MAX_HANGING = 7
MAX_CROWN = 4
MAX_GIFT = 6
MAX_GARLAND = 6


class ToysForm(forms.Form):
    hanging = forms.IntegerField(min_value=0, max_value=MAX_HANGING)
    crown = forms.IntegerField(min_value=0, max_value=MAX_CROWN)
    gift = forms.IntegerField(min_value=0, max_value=MAX_GIFT)
    garland = forms.IntegerField(min_value=0, max_value=MAX_GARLAND)
