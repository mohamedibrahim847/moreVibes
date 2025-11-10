from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.conf import settings
import spotipy
from spotipy.oauth2 import SpotifyOAuth


def get_spotify_oauth():
    return SpotifyOAuth(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIFY_REDIRECT_URI,
        scope=" ".join([
            "user-read-private",
            "user-read-email",
            "user-top-read",
            "user-read-recently-played",
            "playlist-read-private",
            "playlist-modify-public",
            "user-library-read",
            ])
        )


def login(request):
    sp_oauth = get_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


def callback(request):
    sp_oauth = get_spotify_oauth()
    code = request.GET.get('code')
    
    if code:
        token_info = sp_oauth.get_access_token(code)
        request.session['token_info'] = token_info
        return redirect('home')
    return HttpResponse("Error: No code provided")


def home(request):
    token_info = request.session.get('token_info')
    
    if not token_info:
        return HttpResponse('<a href="/login">Login with Spotify</a>')
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    user = sp.current_user()
    
    return HttpResponse(f"Hello, {user['display_name']}!")

