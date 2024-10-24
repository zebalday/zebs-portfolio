from django.shortcuts import render, redirect
from requests import Request, post
import dotenv, os, base64
from .utils import update_or_create_user_tokens

dotenv.load_dotenv()


# Variables
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SCRT = os.getenv('CLIENT_SCRT')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')


# Authentication URL
def get_auth_url():
    
    scope = """
            playlist-read-collaborative
            playlist-read-private
            user-follow-read
            user-library-read
            user-read-currently-playing
            user-read-playback-state
            user-read-recently-played
            user-top-read
            """.strip()

    url = Request(
            'GET', 
            'https://accounts.spotify.com/authorize',
            params={
                'scope': scope,
                'response_type': 'code',
                'redirect_uri': SPOTIFY_REDIRECT_URI,
                'client_id': CLIENT_ID,
            }
        ).prepare().url

    return url


# Spotify callback
def spotify_callback(request):

    # Catching code or error in request
    code = request.GET.get('code')
    error = request.GET.get('error')

    # Sending authorization credentials
    response = post(
                'https://accounts.spotify.com/api/token',
                data = {
                    'grant_type' : 'authorization_code',
                    'code' : code,
                    'redirect_uri' : SPOTIFY_REDIRECT_URI,
                    'client_id': CLIENT_ID,
                    'client_secret': CLIENT_SCRT,
                },
                headers = {
                    'content-type': 'application/x-www-form-urlencoded',
                    'Authorization': 'Basic ' + base64.b64encode((CLIENT_ID + ':' + CLIENT_SCRT).encode()).decode()
                }
            )
    
    response = response.json()
    print(f"Callback: {response}")

    # Fetching data from response
    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')

    # Verify if there's an active user session
    if not request.session.exists(request.session.session_key):
        request.session.create()

    # Saving tokens on the database
    update_or_create_user_tokens(
        request.session.session_key, 
        access_token=access_token, 
        token_type=token_type, 
        expires_in=expires_in, 
        refresh_token=refresh_token
    )

    return redirect("portfolio:index")