"""Get Playlist information and analyse."""

from copy import deepcopy

from src.access_token import AccessToken
from src.outbound_requests import (
    pull_playlist_data,
    pull_tracks_audio_features_r,
    request_access_token,
)
from src.playlist import Playlist


def clean_raw_playlist_data(playlist: dict) -> dict:
    """Return dict with playlist data.

    Removes the excess data from request that isn't needed."""
    keys = [
        "name",
        "collaborative",
        "description",
        "followers",
        "id",
        "public",
        "tracks",
    ]
    playlist_copy = deepcopy(playlist)
    clean = {}
    for key in keys:
        clean[key] = playlist_copy[key]
    return clean


def clean_up_track_features(raw_feature_data: dict) -> tuple:
    """Remove keys that aren't needed."""
    feature_copy = raw_feature_data.copy()
    keys = [
        "acousticness",
        "danceability",
        "energy",
        "instrumentalness",
        "key",
        "liveness",
        "loudness",
        "mode",
        "speechiness",
        "tempo",
        "time_signature",
        "valence",
    ]
    clean = {}
    for key in keys:
        clean[key] = feature_copy[key]
    return (feature_copy["id"], clean)


def populate_track_features(playlist: Playlist, cleaned_feature_list: tuple) -> None:
    """Populate track in playlist with the audio features."""
    for id, track_feature in cleaned_feature_list:
        playlist.get_track(id).populate_audio_features(**track_feature)
    return playlist


def analyse_playlists(playlist_id: str) -> None:
    """Trigger the analysis."""
    token = AccessToken(**request_access_token())
    raw_playlist = pull_playlist_data(token.get_token(), playlist_id)

    clean_playlist = clean_raw_playlist_data(raw_playlist)
    playlist = Playlist(**clean_playlist)
    print(f"Playlist: {playlist.name}")
    print(f"Description: {playlist.description}")
    print(f"Total Tracks: {playlist.total_tracks}")
    print(f"Is Public: {playlist.public}")
    track_ids = playlist.get_all_track_ids()
    audio_features_list = pull_tracks_audio_features_r(token.get_token(), track_ids)
    cleaned_features = list(map(clean_up_track_features, audio_features_list))
    playlist = populate_track_features(playlist, cleaned_features)
    print(f"Playlist: {playlist.name}")
    print(f"Description: {playlist.description}")
    print(f"Total Tracks: {playlist.total_tracks}")
    for id, track in playlist._tracks.items():
        print(
            f"Track: {track._name}, by {track._artists[0]['name']}. Time signature: {track._time_signature}/4"
        )
