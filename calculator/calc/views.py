from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ToysForm
from .utils import form_handler


def index(request):
    """Выводит шаблон главной страницы."""
    if request.user.is_authenticated:
        return redirect('calc:national')
    return render(request, 'calc/index.html')


@login_required
def national(request):
    """Выводит шаблон страницы отечественной коллекции."""

    username = request.user.username
    form = ToysForm(request.POST or None)
    user_data, is_calc = form_handler(request, form, username, 'national')
    if is_calc:
        return redirect('recommendations:recommendations')
    context = {'user_data': user_data}
    return render(request, 'calc/collections.html', context)


@login_required
def christmas(request):
    """Выводит шаблон страницы рождественской коллекции."""

    username = request.user.username
    form = ToysForm(request.POST or None)
    user_data, is_calc = form_handler(request, form, username, 'christmas')
    if is_calc:
        return redirect('recommendations:recommendations')
    context = {'user_data': user_data}
    return render(request, 'calc/collections.html', context)


@login_required
def eastern(request):
    """Выводит шаблон страницы восточной коллекции."""

    username = request.user.username
    form = ToysForm(request.POST or None)
    user_data, is_calc = form_handler(request, form, username, 'eastern')
    if is_calc:
        return redirect('recommendations:recommendations')
    context = {'user_data': user_data}
    return render(request, 'calc/collections.html', context)


@login_required
def magic(request):
    """Выводит шаблон страницы сказочной коллекции."""

    username = request.user.username
    form = ToysForm(request.POST or None)
    user_data, is_calc = form_handler(request, form, username, 'magic')
    if is_calc:
        return redirect('recommendations:recommendations')
    context = {'user_data': user_data}
    return render(request, 'calc/collections.html', context)
