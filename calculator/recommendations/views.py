from calc.main_calc import pd
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from mongodb.mongo_init import results


def recommendations(request):
    """Выводит шаблон страницы рекомендаций."""
    username = request.user.username
    user_result = results.find_one({'username': username})['result']
    context = {'user_result': user_result}
    print(context)
    return render(request, 'recommendations/recommendations.html', context)
