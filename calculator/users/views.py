from captcha.fields import CaptchaField
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from tiny_db.views import add_new_user_collection

from .forms import CreationForm


class SignUp(CreateView):
    """
    Класс представления для регистрации новых пользователей.
    """
    form_class = CreationForm
    success_url = reverse_lazy('calc:index')
    template_name = 'users/signup.html'
    captcha = CaptchaField()

    def form_valid(self, form):
        """
        Переопределение метода form_valid для автоматической аутентификации
        пользователя после успешной регистрации и создания пустой коллекции
        для нового пользователя.

        Args:
            form (Form): Форма, содержащая данные пользователя.

        Returns:
            HttpResponse: Ответ после успешной обработки формы.
        """

        response = super().form_valid(form)
        login(self.request, self.object)  # Войти в систему пользователем
        username = self.object.username
        add_new_user_collection(username)
        return response
