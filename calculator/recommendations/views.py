from calc.main_calc import pd
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from mongodb.mongo_init import results


def recommendations(request):
    """Выводит шаблон страницы рекомендаций."""
    username = request.user.username
    result = results.find_one({'username': username})
    user_result = result.get('result')
    user_advice = result.get('advice')
    user_advice_2 = result.get('advice_2')
    context = {
        'user_result': user_result,
        'user_advice': user_advice,
        'user_advice_2': user_advice_2,
    }
    # print(context)
    return render(request, 'recommendations/recommendations.html', context)
