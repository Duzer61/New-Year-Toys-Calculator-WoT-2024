from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


def recommendations(request):
    """Выводит шаблон страницы рекомендаций."""

    return render(request, 'recommendations/recommendations.html')