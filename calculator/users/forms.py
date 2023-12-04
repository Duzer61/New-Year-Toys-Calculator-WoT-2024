from captcha.fields import CaptchaField
from django.contrib.auth.forms import UserCreationForm

from .models import User


class CreationForm(UserCreationForm):
    captcha = CaptchaField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',)
