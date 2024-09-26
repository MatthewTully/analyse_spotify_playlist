"""All the Outbound HTTPS requests to Spotify."""

from requests import get, post

from analyse_spotify_playlist.config import (
    CLIENT_ID,
    CLIENT_SECRET,
    SPOTIFY_ACCOUNTS_URL,
    SPOTIFY_API_URL,
)
from analyse_spotify_playlist.playlist import Playlist
from analyse_spotify_playlist.utils import performance_timer


def request_access_token() -> dict:
    """Request access token from Spotify."""
    body = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    res = post(SPOTIFY_ACCOUNTS_URL, body, headers=headers)
    res.raise_for_status()

    return res.json()


def set_auth_header(token: str) -> dict:
    """Set the auth header for requests to api."""
    return {"Authorization": f"Bearer {token}"}


def pull_playlist_data(token: str, playlist_id: str) -> dict:
    """Request Playlist data from Spotify

    Args:
        token (str): Authorisation token for the request
        playlist_id (str): Id for the playlist.

    Returns:
        raw playlist data (dict)
    """
    url = f"{SPOTIFY_API_URL}playlists/{playlist_id}"
    res = get(url, headers=set_auth_header(token))
    res.raise_for_status()

    return res.json()


def pull_next_set_of_tracks(token: str, playlist: Playlist) -> None:
    """Use the 'next' Url to fetch the next set of Tracks for the playlist."""
    url = playlist.next_url
    res = get(url, headers=set_auth_header(token))
    res.raise_for_status()
    # print(f"Response took - {res.elapsed.total_seconds()}s")

    tracks = res.json()
    playlist.add_tracks(tracks)
    if playlist.next_url:
        pull_next_set_of_tracks(token, playlist)


# @performance_timer
def pull_tracks_audio_features_r(token: str, track_ids: list[str]) -> list:
    """Recursively Split id list down to size and make the request."""
    if len(track_ids) <= 100:
        return audio_feature_request(token, track_ids)

    shortened_list = track_ids[0:100]
    remaining_list = track_ids[100:]
    features = []
    features.extend(audio_feature_request(token, shortened_list))
    features.extend(pull_tracks_audio_features_r(token, remaining_list))
    return features


def audio_feature_request(token: str, track_ids: list[str]) -> list:
    """Request the audio features of the provided track_ids."""
    if len(track_ids) > 100:
        raise ValueError("too many track ids to request. Maximum is 100")
    if len(track_ids) == 0:
        return []
    id_string = ",".join(track_ids)

    url = f"{SPOTIFY_API_URL}audio-features"
    params = {"ids": id_string}
    res = get(url, params=params, headers=set_auth_header(token))
    res.raise_for_status()

    return res.json()["audio_features"]
