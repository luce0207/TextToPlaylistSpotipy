import spotipy
from spotipy.oauth2 import SpotifyOAuth
import csv
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.abspath(f'{os.environ["HOME"]}/.env'))


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.environ["CLIENT_ID"],
    client_secret=os.environ["CLIENT_SECRET"],
    redirect_uri=os.environ["REDIRECT_URI"],
    scope="playlist-modify-public playlist-modify-private"
))
user_id = sp.me()["id"]


def create_playlist(playlist_name:str) -> str: 
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
    playlist_id = playlist["id"]
    print(f"Playlist '{playlist_name}' created!")
    return playlist_id


def add_tracks(playlist_id:str, csv_filename:str):
    songs = []

    with open(csv_filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2:
                song_title, artist = row[0], row[1]
                songs.append(f"{song_title} - {artist}")

    track_uris = []
    for song in songs:
        results = sp.search(q=song, type="track", limit=1)
        if len(results["tracks"]["items"])>0:
            track_uris.append(results["tracks"]["items"][0]["uri"])
            print(f"Found: {song}")
        else:
            print(f"No results found for '{song}'")

    
    def chunk_list(lst, size):
        for i in range(0, len(lst), size):
            yield lst[i:i + size]

    added_nb = 0
    for batch in chunk_list(track_uris, 100):
        sp.playlist_add_items(playlist_id, batch)
        added_nb += len(batch)

    print(f"Added {added_nb} songs to the playlist.")

        
        