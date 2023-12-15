from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from .forms import ChristmasForm, EasternForm, MagicForm, NationalForm
from .utils import form_handler
from .models import UserAlbums


def index(request):
    """Выводит шаблон главной страницы."""
    if request.user.is_authenticated:
        return redirect('calc:national')
    return render(request, 'calc/index.html')


@csrf_exempt
@login_required
def national(request):
    """Выводит шаблон страницы отечественной коллекции."""

    user = request.user
    album = UserAlbums.objects.get_or_create(user=user)
    form = NationalForm(request.POST or None, instance=album)
    if form.is_valid():
        form.save()
        if 'calculate' in request.POST:
            return redirect('recommendations:recommendations')
    context = {'form': form}
    return render(request, 'calc/collections.html', context)


@csrf_exempt
@login_required
def christmas(request):
    """Выводит шаблон страницы рождественской коллекции."""

    user = request.user
    album = UserAlbums.objects.get_or_create(user=user)
    form = ChristmasForm(request.POST or None, instance=album)
    if form.is_valid():
        form.save()
        if 'calculate' in request.POST:
            return redirect('recommendations:recommendations')
    context = {'form': form}
    return render(request, 'calc/collections.html', context)


@csrf_exempt
@login_required
def eastern(request):
    """Выводит шаблон страницы восточной коллекции."""

    user = request.user
    album = UserAlbums.objects.get_or_create(user=user)
    form = EasternForm(request.POST or None, instance=album)
    if form.is_valid():
        form.save()
        if 'calculate' in request.POST:
            return redirect('recommendations:recommendations')
    context = {'form': form}
    return render(request, 'calc/collections.html', context)


@csrf_exempt
@login_required
def magic(request):
    """Выводит шаблон страницы сказочной коллекции."""

    user = request.user
    album = UserAlbums.objects.get_or_create(user=user)
    form = MagicForm(request.POST or None, instance=album)
    if form.is_valid():
        form.save()
        if 'calculate' in request.POST:
            return redirect('recommendations:recommendations')
    context = {'form': form}
    return render(request, 'calc/collections.html', context)
