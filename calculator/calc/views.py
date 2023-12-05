from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render


def national(request):
    """Выводит шаблон страницы отечественной коллекции."""


    return render(request, 'calc/national.html')


@login_required
def christmas(request):
    """Выводит шаблон страницы рождественской коллекции."""

    return render(request, 'calc/christmas.html')


@login_required
def eastern(request):
    """Выводит шаблон страницы восточной коллекции."""

    return render(request, 'calc/eastern.html')


@login_required
def magic(request):
    """Выводит шаблон страницы сказочной коллекции."""

    return render(request, 'calc/magic.html')
