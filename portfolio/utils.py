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
def refresh_token(access_token = None):

    # Data to refresh
    spotify_token = SpotifyToken.objects.get(access_token=access_token) if access_token else SpotifyToken.objects.last()
    refresh_token = spotify_token.refresh_token

    print(f"REFRESHING EXPIRES IN: {spotify_token.expires_in}")
    print(f"REFRESHING ID: {spotify_token.id}")

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
    print(f"NEW ACCESS TOKEN: {response['access_token'][:15]}")
    print(f"EXPIRES IN: {expires_in}")

    # Return new access token
    return response['access_token']



# Check if token is valid
def check_valid_token(access_token):

    #print(f"CHECKING: {access_token[:15]}")
    
    token = SpotifyToken.objects.get(access_token=access_token)
    valid = True if token.expires_in > timezone.now() else False

    return valid

    """ return {
        'is_auth' : valid,
        'token_id':token.id,
        'token':token.access_token,
        'expires_in':token.expires_in,
        'timezone_now':timezone.now()
    } """



# Get valid token
def get_valid_token(access_token = None):
    
    # Get access token
    access_token = access_token if access_token else SpotifyToken.objects.last().access_token
    
    # Return valid token
    if not check_valid_token(access_token):
        return refresh_token(access_token)
    
    return access_token



# Get current playing song
def get_current_song(access_token):

    # Valid access token
    access_token = get_valid_token(access_token)

    # Petition
    # CODE 204 --> No message body means no song playing.
    endpoint = 'https://api.spotify.com/v1/me/player/currently-playing'

    response = get(
        url=endpoint,
        headers={
            'Content-Type':'application/json',
            'Authorization': f'Bearer {access_token}'
        }
    )

    print(response.status_code)
    #print(response.content)

    if response.status_code == 200:
        response = response.json()
        #print(f"Current playing: {response}")
        return {'currently_playing' : True, 'track' : response}
    
    return {'currently_playing' : False, 'track' : None}



# Get recently played tracks
def get_recently_played(access_token):
    
    # Valid access token
    access_token = get_valid_token(access_token)

    # Petition
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

    print(response.status_code)

    if response.status_code == 200:
        response = response.json()
        #print(f"Recently played: {response}")
        #print(len(response['items']))
        return {'recently_exists' : True, 'tracks' : response['items']}
    
    return {'recently_exists' : False, 'tracks' : None}
