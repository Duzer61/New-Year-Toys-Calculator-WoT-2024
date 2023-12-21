from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from calc.views import csrf_exempt
from .main_calc import main_calc
from .utils import get_advice
from .models import AlbumSelect
from .forms import AlbumSelectForm


@csrf_exempt
@login_required
def recommendations(request):
    """Выводит шаблон страницы рекомендаций."""

    user_id = request.user.id
    album_select, created = AlbumSelect.objects.get_or_create(user_id=user_id)
    form = AlbumSelectForm(request.POST or None, instance=album_select)
    if form.is_valid():
        album_select = form.save(commit=False)
        album_select.user = request.user
        album_select.save()
        return redirect('recommendations:recommendations')
    tables_data, min_data = main_calc(user_id)
    advice, advice_2 = get_advice(min_data)
    context = {
        'user_result': tables_data,
        'user_advice': advice,
        'user_advice_2': advice_2,
        'form': form,
    }
    return render(request, 'recommendations/recommendations.html', context)
