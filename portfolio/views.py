from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Project

# Create your views here.
class index(TemplateView):

    template_name = 'portfolio/index.html'
    context = {}

    def get(self, request):
        
        self.context['projects'] = Project.objects.filter(public = True)
        
        return render(request, self.template_name, self.context)
    



