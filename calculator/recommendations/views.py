from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .main_calc import main_calc
from .utils import get_advice


@login_required
def recommendations(request):
    """Выводит шаблон страницы рекомендаций."""

    user_id = request.user.id
    tables_data, min_data = main_calc(user_id)
    advice, advice_2 = get_advice(min_data)
    context = {
        'user_result': tables_data,
        'user_advice': advice,
        'user_advice_2': advice_2,
    }
    return render(request, 'recommendations/recommendations.html', context)
