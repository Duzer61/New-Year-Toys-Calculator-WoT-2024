from django import forms
from .models import AlbumSelect


class AlbumSelectForm(forms.ModelForm):
    """
    Форма для выбора настроек пользователя.
    """
    class Meta:
        model = AlbumSelect
        fields = [
            'national',
            'eastern',
            'magic',
            'christmas',
        ]
