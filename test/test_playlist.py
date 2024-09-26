import unittest
import unittest.mock
from copy import deepcopy
from test.mock_data import MOCK_PLAYLIST_RESPONSE

from analyse_spotify_playlist.playlist import Playlist
from analyse_spotify_playlist.track import Track


class TestPlaylistClass(unittest.TestCase):

    def setup_mock_playlist(self):
        mock_playlist = deepcopy(MOCK_PLAYLIST_RESPONSE)
        expected_keys = [
            "name",
            "owner",
            "collaborative",
            "description",
            "followers",
            "id",
            "public",
            "tracks",
        ]
        mock_res = {}
        for key in expected_keys:
            mock_res[key] = mock_playlist[key]
        playlist = Playlist(**mock_res)
        return playlist

    def test_constructor(self):
        mock_playlist = deepcopy(MOCK_PLAYLIST_RESPONSE)
        expected_keys = [
            "name",
            "owner",
            "collaborative",
            "description",
            "followers",
            "id",
            "public",
            "tracks",
        ]
        mock_res = {}
        for key in expected_keys:
            mock_res[key] = mock_playlist[key]
        playlist = Playlist(**mock_res)
        self.assertIsInstance(playlist, Playlist)

    def test_get_track_with_valid_id(self):
        playlist = self.setup_mock_playlist()
        valid_id = "4rzfv0JLZfVhOhbSQ8o5jZ"
        track = playlist.get_track(valid_id)
        self.assertIsInstance(track, Track)

    def test_get_track_with_invalid_id(self):
        playlist = self.setup_mock_playlist()
        self.assertIsNone(playlist.get_track(1))
        self.assertIsNone(playlist.get_track(None))

    def test_get_all_track_ids(self):
        playlist = self.setup_mock_playlist()
        self.assertGreater(len(playlist.get_all_track_ids()), 0)
        self.assertEqual(len(playlist.get_all_track_ids()), len(playlist._tracks))
