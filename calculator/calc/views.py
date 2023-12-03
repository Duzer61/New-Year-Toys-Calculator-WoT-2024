from django.shortcuts import get_object_or_404, redirect, render


def index(request):
    """Выводит шаблон главной страницы."""

    return render(request, 'calc/index.html')
