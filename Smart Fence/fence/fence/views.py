from django.views.generic import TemplateView

class HomePage(TemplateView):
  template_name = 'index.html'

class TestPage(TemplateView):
  template_name = 'test.html'

class ThanksPage(TemplateView):
  template_name = 'thanks.html'

class AboutPage(TemplateView):
  template_name = 'about.html'

