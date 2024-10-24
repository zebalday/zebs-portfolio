from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
from .models import Project
from pyhub.GitHubAPI import GitHubApi
import dotenv
import os


dotenv.load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

class index(TemplateView):

    template_name = 'portfolio/index.html'
    context = {}

    def get(self, request):
        
        self.context['projects'] = Project.objects.filter(public = True)
        return render(request, self.template_name, self.context)


def get_last_commits(request):
    last_commits = GitHubApi(GITHUB_TOKEN).getLastCommits('zebalday', 3)
    return JsonResponse(last_commits)
    



