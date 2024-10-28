from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
from .models import Project, SpotifyToken
from .serializers import SpotifyTokensSerializer
from .utils import save_tokens, refresh_token, get_current_song, get_recently_played
from pyhub.GitHubAPI import GitHubApi
from requests import get, post, Request
import dotenv
import os
import base64



# Variables
dotenv.load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
SPOTIFY_M = os.getenv('SPOTIFY_M')
SPOTIFY_P = os.getenv('SPOTIFY_P')
BASE_URL = "https://api.spotify.com/v1/me"
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')



# Render index templates
class index(TemplateView):

    template_name = 'portfolio/index.html'
    context = {}

    def get(self, request):
        
        # Get access token
        access_token = request.session['access_token'] if 'access_token' in request.session else refresh_token()
        
        # Context
        self.context['projects'] = Project.objects.filter(public = True)
        self.context['login_url'] = request_auth()
        self.context['current_song'] = get_current_song(access_token)
        self.context['recently_played'] = get_recently_played(access_token)

        return render(request, self.template_name, self.context)



# Get my last commits
def get_last_commits(request):
    last_commits = GitHubApi(GITHUB_TOKEN).getLastCommits('zebalday', 3)
    return JsonResponse(last_commits)



# Request authorization to access data
def request_auth():
    
    auth_url = 'https://accounts.spotify.com/authorize?'
    scope = 'user-read-currently-playing'

    url = Request(
        method='GET',
        url=auth_url,
        params={
            'scope':scope,
            'client_id':CLIENT_ID,
            'redirect_uri':REDIRECT_URI,
            'response_type':'code'
        }
    ).prepare().url

    return url



# Request tokens after login
# CALLBACK
def spotify_callback(request):

    if request.GET['code']:
        # Vars
        code = request.GET['code']
        tokens_url = 'https://accounts.spotify.com/api/token'

        # POST - Request tokens
        response = post(
            url=tokens_url,
            headers={
                'Authorization':'Basic ' + base64.b64encode((CLIENT_ID + ':' + CLIENT_SECRET).encode()).decode(),
                'Content-Type':'application/x-www-form-urlencoded'
            },
            params={
                'grant_type':'authorization_code',
                'code':code,
                'redirect_uri':REDIRECT_URI
            }
        )

        # Save response tokens
        response = response.json()
        save_tokens(response)

        # Set session token 
        if not 'access_token' in request.session:
            request.session['access_token'] = response['access_token']

        # Show data
        spotify_token = SpotifyToken.objects.get(access_token = response['access_token'])
        spotify_token = SpotifyTokensSerializer(spotify_token).data
        return JsonResponse({'response':response, 'object':spotify_token})



# Fetch current song
def current_song(request):
    
    access_token = request.session['access_token'] if 'access_token' in request.session else refresh_token()
    track = get_current_song(access_token)
    return JsonResponse(track)



# Fetch recently played
def recently_played(request):

    access_token = request.session['access_token'] if 'access_token' in request.session else refresh_token()
    tracks = get_recently_played(access_token)
    return JsonResponse(tracks)


