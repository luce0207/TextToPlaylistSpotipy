import spotipy
from spotipy.oauth2 import SpotifyOAuth
import csv

CLIENT_ID = "030c2660bef442b3877628e346de5244"
CLIENT_SECRET = "c106ee717b3446519cd792dd9ea35223"
REDIRECT_URI = "http://localhost:8888/callback"

# Authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="playlist-modify-public playlist-modify-private"
))

# Get the current user's Spotify ID
user_id = sp.me()["id"]

# Create a new playlist
playlist_name = input("Type in a very cool playlist name: ")
playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
playlist_id = playlist["id"]
print(f"Playlist '{playlist_name}' created!")

# Read songs from CSV file
csv_filename = input("Enter your CSV file name with the extension: ")
songs = []

try:
    with open(csv_filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file)  # Skip header row if it exists
        for row in reader:
            if len(row) >= 2:  # Ensure there are at least 2 columns
                song_title, artist = row[0], row[1]
                songs.append(f"{song_title} - {artist}")
except FileNotFoundError:
    print("CSV file not found. Make sure 'songs.csv' is in the correct directory.")
    exit()

# Searching for the songs
track_uris = []
for song in songs:
    results = sp.search(q=song, type="track", limit=1)
    if results["tracks"]["items"]:
        track_uri = results["tracks"]["items"][0]["uri"]
        track_uris.append(track_uri)
        print(f"Found: {song}")

# Adding songs
if track_uris:
    # Function to split the track URIs into chunks of 100
    def chunk_list(lst, size):
        for i in range(0, len(lst), size):
            yield lst[i:i + size]

    # Add songs in batches of 100
    for batch in chunk_list(track_uris, 100):
        sp.playlist_add_items(playlist_id, batch)
        print(f"Added {len(batch)} songs to the playlist.")

    print("Songs added to the playlist!")
else:
    print(f"No results found for '{song}'")
    track_uri = None