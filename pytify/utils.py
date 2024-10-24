
from .models import SpotifyToken
from django.utils import timezone
from datetime import timedelta
from requests import post, put, get
from .serializers import SpotifyTokensSerializer
import dotenv, os

dotenv.load_dotenv()


# Variables
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SCRT = os.getenv('CLIENT_SCRT')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')



# Verify is there're saved tokens associated to an user session.
def get_user_tokens(session_id):

    print(f"Get User Tokens | Session ID: {session_id}")

    try:
        user_tokens = SpotifyToken.objects.get(user=session_id)
        return user_tokens
    except:
        print('No user tokens.')
        return None



# Create or update user tokens
def update_or_create_user_tokens(
        session_id, 
        access_token, 
        token_type, 
        expires_in, 
        refresh_token
    ):
    
    # Get current session tokens & calc. expiring time.
    tokens = get_user_tokens(session_id)
    expires_in = timezone.now() + timedelta(seconds=expires_in)
    
    
    # Update tokens
    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token', 'refresh_token', 'expires_in','token_type'])
        print("Acción Actualizar")

    # Create tokens
    else:
        tokens = SpotifyToken(
            user=session_id, 
            access_token=access_token, 
            refresh_token=refresh_token, 
            token_type=token_type, 
            expires_in=expires_in
        ).save()

        print("Nueva Sesión Guardada")
        print(type(SpotifyToken.objects.get(user=session_id)))



# Check if user is authenticated (false if else) & 
# its token hasn't expired (refresh if else)
def is_spotify_authenticated(session_id):
    
    tokens = get_user_tokens(session_id)
    
    if (tokens) and (tokens.expires_in <= timezone.now()):
        refresh_spotify_token(session_id)
        return True
    return False



# Refresh spotify token
def refresh_spotify_token(session_id):
    
    refresh_token = get_user_tokens(session_id).refresh_token

    response = post('https://accounts.spotify.com/api/token',
                    data = {
                        'grant_type':'refresh_token',
                        'refresh_token': refresh_token,
                        'client_id': CLIENT_ID,
                        'client_secret': CLIENT_SCRT
                        },
                    headers={
                        'Content-Type': 'application/x-www-form-urlencoded',
                        }
                    )
    
    #print(response.status_code)
    response = response.json()
    print(f"Refresh: {response}")

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')
    
    #print(refresh_token)

    try:
        update_or_create_user_tokens(
            session_id, 
            access_token, 
            token_type, expires_in, 
            refresh_token
        )

    except Exception as ex:
        print(ex)