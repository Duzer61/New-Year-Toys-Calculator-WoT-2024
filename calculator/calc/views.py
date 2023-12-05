from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from mongodb.mongo_init import collection
from users.models import User


def index(request):
    """Выводит шаблон главной страницы."""
    if request.user.is_authenticated:
        return redirect('calc:national')
    return render(request, 'calc/index.html')


@login_required
def national(request):
    """Выводит шаблон страницы отечественной коллекции."""

    username = request.user.username
    user_data = collection.find_one(
        {'username': username},
        {'collection.national': 1}
    )['collection']['national']

    print(user_data)
    if request.method == 'POST':
        crown = int(request.POST.get('crown'))
        garland = int(request.POST.get('garland'))
        hanging = int(request.POST.get('hanging'))
        gift = int(request.POST.get('gift'))

        new_data = {
            'crown': crown,
            'garland': garland,
            'hanging': hanging,
            'gift': gift
        }

        collection.update_one(
            {'username': username},
            {'$set': {'collection.national': new_data}}
        )

    return render(request, 'calc/collections.html')


@login_required
def christmas(request):
    """Выводит шаблон страницы рождественской коллекции."""

    username = request.user.username
    user_data = collection.find_one(
        {'username': username},
        {'collection.christmas': 1}
    )['collection']['christmas']

    print(user_data)
    if request.method == 'POST':
        crown = int(request.POST.get('crown'))
        garland = int(request.POST.get('garland'))
        hanging = int(request.POST.get('hanging'))
        gift = int(request.POST.get('gift'))

        new_data = {
            'crown': crown,
            'garland': garland,
            'hanging': hanging,
            'gift': gift
        }

        collection.update_one(
            {'username': username},
            {'$set': {'collection.christmas': new_data}}
        )

    return render(request, 'calc/collections.html')


@login_required
def eastern(request):
    """Выводит шаблон страницы восточной коллекции."""

    username = request.user.username
    user_data = collection.find_one(
        {'username': username},
        {'collection.eastern': 1}
    )['collection']['eastern']

    print(user_data)
    if request.method == 'POST':
        crown = int(request.POST.get('crown'))
        garland = int(request.POST.get('garland'))
        hanging = int(request.POST.get('hanging'))
        gift = int(request.POST.get('gift'))

        new_data = {
            'crown': crown,
            'garland': garland,
            'hanging': hanging,
            'gift': gift
        }

        collection.update_one(
            {'username': username},
            {'$set': {'collection.eastern': new_data}}
        )
    return render(request, 'calc/collections.html')


@login_required
def magic(request):
    """Выводит шаблон страницы сказочной коллекции."""

    username = request.user.username
    user_data = collection.find_one(
        {'username': username},
        {'collection.magic': 1}
    )['collection']['magic']

    print(user_data)
    if request.method == 'POST':
        crown = int(request.POST.get('crown'))
        garland = int(request.POST.get('garland'))
        hanging = int(request.POST.get('hanging'))
        gift = int(request.POST.get('gift'))

        new_data = {
            'crown': crown,
            'garland': garland,
            'hanging': hanging,
            'gift': gift
        }

        collection.update_one(
            {'username': username},
            {'$set': {'collection.magic': new_data}}
        )
    return render(request, 'calc/collections.html')
