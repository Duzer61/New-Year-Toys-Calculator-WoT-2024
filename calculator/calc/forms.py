from django import forms

from .constants import MAX_CROWN, MAX_GARLAND, MAX_GIFT, MAX_HANGING


class ToysForm(forms.Form):
    hanging = forms.IntegerField(min_value=0, max_value=MAX_HANGING)
    crown = forms.IntegerField(min_value=0, max_value=MAX_CROWN)
    gift = forms.IntegerField(min_value=0, max_value=MAX_GIFT)
    garland = forms.IntegerField(min_value=0, max_value=MAX_GARLAND)
