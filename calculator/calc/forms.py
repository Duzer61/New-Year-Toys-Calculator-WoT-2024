from django import forms

# Максимальные количество игрушек в каждой категории
MAX_CROWN = 5
MAX_GARLAND = 5
MAX_HANGING = 5
MAX_GIFT = 5


class ToysForm(forms.Form):
    crown = forms.IntegerField(min_value=0, max_value=MAX_CROWN)
    garland = forms.IntegerField(min_value=0, max_value=MAX_GARLAND)
    hanging = forms.IntegerField(min_value=0, max_value=MAX_HANGING)
    gift = forms.IntegerField(min_value=0, max_value=MAX_GIFT)

    # def get_forms_data(self, request):
    #     """
    #     Получает данные из формы и возвращает в виде словаря
    #     с провалидированными значениями.
    #     """
    #     form = self.request.POST
    #     if form.is_valid():
    #         forms_data = form.cleaned_data
    #     else:
    #         forms_data = {}
    #     return forms_data
