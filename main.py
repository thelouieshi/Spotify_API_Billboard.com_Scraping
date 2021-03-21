import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from bs4 import BeautifulSoup

date = input("Which day's top 100 do you want? YYYY-MM-DD:\n")

# option to export environment variables,
SPOTIFY_CLIENT_ID = "57d2947b5bd04feeab9f74941d5e5c91"
SPOTIFY_CLIENT_SECRET = "d000698dd72e4f8e9ea777c75ea45725"

respond = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
web_content = respond.text
billboard_soup = BeautifulSoup(web_content, "html.parser")

# Capture song names into a list
song_names_output = billboard_soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
song_names = [song_tag.getText() for song_tag in song_names_output]

# capture artist names into a list
artist_output = billboard_soup.find_all(name="span", class_="chart-element__information__artist text--truncate color--secondary")
artist_name = [artist_tag.getText() for artist_tag in artist_output]

# Spotify authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]

song_uris = []
year = date.split("-")[0]
for song in song_names:
    output = sp.search(q=f"track:{song} year:{year}", type="track")
    # some songs are not on Spotify
    try:
        uri = output["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# create a playlist simply named as "{date} Billboard 100"
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# add items to the playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

# For more of my projects, fun games and useful applicatons, 
# please visit: https://github.com/thlouieshi?tab=repositories
