from django.utils import timezone
from datetime import timedelta
from .models import SpotifyToken
from .serializers import SpotifyTokensSerializer
from requests import post, get
import base64
import os
import dotenv



# Variables
dotenv.load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
SPOTIFY_M = os.getenv('SPOTIFY_M')
SPOTIFY_P = os.getenv('SPOTIFY_P')
BASE_URL = "https://api.spotify.com/v1/me"
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')



# Save new tokens
def save_tokens(response):

    # Expiry Time
    expires_in = response['expires_in']
    expires_in = timezone.now() + timedelta(seconds=expires_in)
    
    # Tokens data
    token_type =  response['token_type']
    access_token = response['access_token']
    refresh_token =  response['refresh_token']
    expires_in =  expires_in
    scope = response['scope']

    # Debug
    print(f"Creating token: {token_type}: Access = {access_token[:9]}; Refresh {refresh_token[:9]}; {expires_in}")

    # Save tokens
    SpotifyToken.objects.create(
        token_type = token_type,
        access_token = access_token,
        refresh_token = refresh_token,
        expires_in = expires_in,
        scope = scope
    )



# Refresh existing tokens
def refresh_token():

    # Data to refresh
    spotify_token = SpotifyToken.objects.first()
    refresh_token = spotify_token.refresh_token

    print(spotify_token.expires_in)
    print(refresh_token)

    # URL
    tokens_url = 'https://accounts.spotify.com/api/token'

    # POST - Request tokens
    response = post(
        url=tokens_url,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        params={
            'grant_type':'refresh_token',
            'refresh_token':refresh_token,
            'client_id':CLIENT_ID,
            'client_secret':CLIENT_SECRET
        }
    )

    response = response.json()
    
    # Expiry Time
    expires_in = response['expires_in']
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    # Update data
    spotify_token.access_token = response['access_token']
    spotify_token.refresh_token = response['refresh_token'] if 'refresh_token' in response else spotify_token.refresh_token
    spotify_token.expires_in = expires_in
    spotify_token.save()
    
    # Debug
    print(f"Refreshing token: {response['access_token'][:9]}; Refresh {refresh_token[:9]}; {expires_in}")

    # Return new access token
    return response['access_token']



# Get current playing song
def get_current_song(access_token):

    # CODE 204 --> No message body means no song playing.

    endpoint = 'https://api.spotify.com/v1/me/player/currently-playing'

    response = get(
        url=endpoint,
        headers={
            'Content-Type':'application/json',
            'Authorization': f'Bearer {access_token}'
        }
    )

    if response.status_code == 200:
        response = response.json()
        print(f"Current playing: {response}")
        return {'currently_playing' : True, 'track' : response}
    
    return {'currently_playing' : False, 'track' : None}



# Get recently played tracks
def get_recently_played(access_token):
    
    endpoint = 'https://api.spotify.com/v1/me/player/recently-played'
    
    response = get(
        url=endpoint,
        headers={
            'Content-Type':'application/json',
            'Authorization': f'Bearer {access_token}'
        },
        params={
            'limit':3
        }
    )

    if response.status_code == 200:
        response = response.json()
        print(f"Recently played: {response}")
        print(len(response['items']))
        return {'recently_exists' : True, 'tracks' : response['items']}
    
    return {'recently_exists' : False, 'tracks' : None}


    
