from django.shortcuts import get_object_or_404, redirect, render


def index(request):
    """Выводит шаблон главной страницы."""

    return render(request, 'calc/index.html')


def christmas(request):
    """Выводит шаблон страницы рождественской коллекции."""

    return render(request, 'calc/christmas.html')


def eastern(request):
    """Выводит шаблон страницы восточной коллекции."""

    return render(request, 'calc/eastern.html')


def magic(request):
    """Выводит шаблон страницы сказочной коллекции."""

    return render(request, 'calc/magic.html')
