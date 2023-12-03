from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    # Перенаправление пользователя на главную после успешной регистрации
    # success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'
