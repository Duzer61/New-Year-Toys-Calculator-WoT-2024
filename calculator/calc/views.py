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
    user_data = collection.find_one({'username': username})

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
