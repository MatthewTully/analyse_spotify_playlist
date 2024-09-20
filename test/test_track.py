import unittest
import unittest.mock
from copy import deepcopy
from test.mock_data import MOCK_TRACK

from src.track import Track


class TestPlaylistClass(unittest.TestCase):
    def setup_mock_track(self):
        mock_track = deepcopy(MOCK_TRACK)
        track = Track(**mock_track)
        return track

    def test_constructor(self):
        mock_track = deepcopy(MOCK_TRACK)
        track = Track(**mock_track)
        self.assertIsInstance(track, Track)

    def test_populate_features(self):
        track = self.setup_mock_track()
        mock_features = {
            "acousticness": 0.011,
            "danceability": 0.696,
            "energy": 0.905,
            "instrumentalness": 0.000905,
            "key": 2,
            "liveness": 0.302,
            "loudness": -2.743,
            "mode": 1,
            "speechiness": 0.103,
            "tempo": 114.944,
            "time_signature": 4,
            "valence": 0.625,
        }
        self.assertIsNone(track._acousticness)
        self.assertIsNone(track._danceability)
        self.assertIsNone(track._energy)
        self.assertIsNone(track._instrumentalness)
        self.assertIsNone(track._key)
        self.assertIsNone(track._liveness)
        self.assertIsNone(track._loudness)
        self.assertIsNone(track._mode)
        self.assertIsNone(track._speechiness)
        self.assertIsNone(track._tempo)
        self.assertIsNone(track._time_signature)
        self.assertIsNone(track._valence)

        track.populate_audio_features(**mock_features)
        self.assertEqual(track._acousticness, mock_features["acousticness"])
        self.assertEqual(track._danceability, mock_features["danceability"])
        self.assertEqual(track._energy, mock_features["energy"])
        self.assertEqual(track._instrumentalness, mock_features["instrumentalness"])
        self.assertEqual(track._key, mock_features["key"])
        self.assertEqual(track._liveness, mock_features["liveness"])
        self.assertEqual(track._loudness, mock_features["loudness"])
        self.assertEqual(track._mode, mock_features["mode"])
        self.assertEqual(track._speechiness, mock_features["speechiness"])
        self.assertEqual(track._tempo, mock_features["tempo"])
        self.assertEqual(track._time_signature, mock_features["time_signature"])
        self.assertEqual(track._valence, mock_features["valence"])
