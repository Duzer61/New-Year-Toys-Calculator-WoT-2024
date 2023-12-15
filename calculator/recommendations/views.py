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
    # username = request.user.username
    # result = results.find_one({'username': username})
    # user_result = result.get('result')
    # user_advice = result.get('advice')
    # user_advice_2 = result.get('advice_2')
    context = {
        'user_result': tables_data,
        'user_advice': advice,
        'user_advice_2': advice_2,
    }
    return render(request, 'recommendations/recommendations.html', context)
