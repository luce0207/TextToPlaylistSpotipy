import unittest
import src.spotify as spotify

#python -m unittest test.test_spotify



#file not found

#invalid file (not csv)

#invalid file (more than / less than 2 columns)

#song not found
PLAYLIST_NAME = "test_import_from_csv"

class TestSpotifyMethods(unittest.TestCase):

    def setUp(self):
        playlists = spotify.sp.user_playlists(user=spotify.user_id)
        #spotify.sp.user_playlist_unfollow.....

    def test_nominal(self):
        playlist_id = spotify.create_playlist("test")
        spotify.add_tracks(playlist_id, "test/test.csv")
        #self.assert_track_nb(2)

    def assert_track_nb(self, expected_nb):
        playlists = spotify.sp.user_playlists()
        #playlists = list(filter(lambda pl: pl.name == PLAYLIST_NAME, playlists)
        self.assertEqual(1, len(playlist))
        playlist_test = playlists[0]
        self.assertEqual(expected_nb, len(spotify.sp.playlist_items))

if __name__ == '__main__':
    unittest.main()