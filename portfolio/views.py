from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone

# Create your views here.
class index(TemplateView):

    template_name = 'portfolio/index.html'
    context = {}

    def get(self, request):
        self.context['timezone'] = timezone.now()
        
        return render(request, self.template_name, self.context)
    



