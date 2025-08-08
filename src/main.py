import spotify



if __name__ == "__main__":
    playlist_name = input("Type in a very cool playlist name: ")
    csv_filename = input("Enter your CSV file name with the extension: ")
    playlist_id = spotify.create_playlist(playlist_name)
    spotify.add_tracks(playlist_id, csv_filename)




