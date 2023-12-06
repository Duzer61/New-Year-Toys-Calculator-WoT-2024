from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from mongodb.initial_data import COLLECTION_DATA
from mongodb.mongo_init import collection
from mongodb.views import add_new_user_collection

from .forms import ToysForm


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
    if form.is_valid():
        forms_data = form.cleaned_data
        collection.update_one(
            {'username': username},
            {'$set': {'collection.national': forms_data}}
        )
    user_data = collection.find_one(
        {'username': username},
        {'collection.national': 1}
    )
    # Проверка, если пользователь был создан ранее, но его коллекции нет в БД
    if user_data:
        user_data = user_data['collection']['national']
    else:  # Если у пользователя нет коллекции, то создаем пустую
        add_new_user_collection(username)
        user_data = COLLECTION_DATA

    context = {'user_data': user_data}
    return render(request, 'calc/collections.html', context)


@login_required
def christmas(request):
    """Выводит шаблон страницы рождественской коллекции."""

    username = request.user.username
    form = ToysForm(request.POST or None)
    if form.is_valid():
        forms_data = form.cleaned_data
        collection.update_one(
            {'username': username},
            {'$set': {'collection.christmas': forms_data}}
        )
    user_data = collection.find_one(
        {'username': username},
        {'collection.christmas': 1}
    )['collection']['christmas']

    context = {'user_data': user_data}
    return render(request, 'calc/collections.html', context)


@login_required
def eastern(request):
    """Выводит шаблон страницы восточной коллекции."""

    username = request.user.username
    form = ToysForm(request.POST or None)
    if form.is_valid():
        forms_data = form.cleaned_data
        collection.update_one(
            {'username': username},
            {'$set': {'collection.eastern': forms_data}}
        )
    user_data = collection.find_one(
        {'username': username},
        {'collection.eastern': 1}
    )['collection']['eastern']

    context = {'user_data': user_data}
    return render(request, 'calc/collections.html', context)


@login_required
def magic(request):
    """Выводит шаблон страницы сказочной коллекции."""

    username = request.user.username
    form = ToysForm(request.POST or None)
    if form.is_valid():
        forms_data = form.cleaned_data
        collection.update_one(
            {'username': username},
            {'$set': {'collection.magic': forms_data}}
        )
    user_data = collection.find_one(
        {'username': username},
        {'collection.magic': 1}
    )['collection']['magic']

    context = {'user_data': user_data}
    return render(request, 'calc/collections.html', context)
