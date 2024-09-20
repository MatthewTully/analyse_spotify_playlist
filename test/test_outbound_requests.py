import unittest
import unittest.mock

from src.outbound_requests import audio_feature_request, pull_tracks_audio_features_r


class MockHTTP:

    def __init__(self, data_to_return):
        self._data = data_to_return

    def json(self) -> dict:
        if isinstance(self._data, dict):
            return self._data
        return dict(self._data)

    def raise_for_status(self) -> None:
        return


class TestOutbound(unittest.TestCase):

    def mock_audio_feature_request(self, token, track_list):
        return [{"id": x} for x in track_list]

    @unittest.mock.patch("src.outbound_requests.audio_feature_request")
    def test_pull_tracks_audio_features_r_1_set(
        self, mock_request: unittest.mock.MagicMock
    ):
        ids = []
        total = 100
        for i in range(total):
            ids.append(i)
        mock_request.side_effect = self.mock_audio_feature_request

        res = pull_tracks_audio_features_r("token", ids)
        self.assertEqual(mock_request.call_count, 1)
        self.assertEqual(len(res), total)

    @unittest.mock.patch("src.outbound_requests.audio_feature_request")
    def test_pull_tracks_audio_features_r_3_set(
        self, mock_request: unittest.mock.MagicMock
    ):
        ids = []
        total = 250
        for i in range(total):
            ids.append(i)
        mock_request.side_effect = self.mock_audio_feature_request

        res = pull_tracks_audio_features_r("token", ids)
        self.assertEqual(mock_request.call_count, 3)
        self.assertEqual(len(res), total)

    @unittest.mock.patch("src.outbound_requests.SPOTIFY_API_URL")
    @unittest.mock.patch("src.outbound_requests.get")
    def test_audio_feature_request(
        self, mock_request: unittest.mock.MagicMock, mock_param
    ):
        ids = ["a", "b", "c", "d", "AAA", "BBB"]
        mock_res = [{"id": x} for x in ids]
        mock_request.return_value = MockHTTP({"audio_features": mock_res})
        mock_param.__str__.return_value = "TEST_URL/"
        res = audio_feature_request("test_token", ids)
        self.assertListEqual(res, mock_res)
        mock_request.assert_called_with(
            "TEST_URL/audio-features",
            params={"ids": "a,b,c,d,AAA,BBB"},
            headers={"Authorization": f"Bearer test_token"},
        )

    @unittest.mock.patch("src.outbound_requests.get")
    def test_audio_feature_request_too_many_exception(
        self, mock_request: unittest.mock.MagicMock
    ):
        with self.assertRaisesRegex(
            ValueError, "too many track ids to request. Maximum is 100"
        ):
            ids = []
            total = 101
            for i in range(total):
                ids.append(i)
            audio_feature_request("token", ids)
        mock_request.assert_not_called()

    @unittest.mock.patch("src.outbound_requests.get")
    def test_audio_feature_request_with_empty_list(
        self, mock_request: unittest.mock.MagicMock
    ):
        res = audio_feature_request("token", [])
        self.assertListEqual(res, [])
        mock_request.assert_not_called()
