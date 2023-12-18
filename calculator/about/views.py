from django.views.generic.base import TemplateView


class AboutView(TemplateView):
    template_name = 'about/about.html'


class AboutAuthorView(TemplateView):
    template_name = 'about/author.html'
