"""Utility functions for app."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from analyse_spotify_playlist.track import Track

from copy import deepcopy
from time import perf_counter

from analyse_spotify_playlist.logger import Log

logger = Log()


def performance_timer(func: function):
    def wrapper(*args, **kwargs):
        start = perf_counter()
        value = func(*args, **kwargs)
        end = perf_counter()
        logger.print(f"{func.__name__} complete. Time taken: {end - start}")
        return value

    return wrapper


def clean_raw_playlist_data(playlist: dict) -> dict:
    """Return dict with playlist data.

    Removes the excess data from request that isn't needed."""
    keys = [
        "name",
        "owner",
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
    if not isinstance(raw_feature_data, dict):
        return (None, None)
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


# @performance_timer
def find_min_max_audio_features(
    track_list: dict[str, Track],
) -> dict[str, list[list[str, float]]]:
    """Find the minimum value for each audio feature, for each track in a list.

    Args:
        track_list (list): list to loop over.
    Return:
        dict: each audio feature as a key with a list of tuple pairs as the value.
        i.e: [(id1, min), (id2, max)]
    """
    min_value = float("inf")
    max_value = float("-inf")
    return_object = {
        "acousticness": [[None, min_value], [None, max_value]],
        "danceability": [[None, min_value], [None, max_value]],
        "energy": [[None, min_value], [None, max_value]],
        "instrumentalness": [[None, min_value], [None, max_value]],
        "liveness": [[None, min_value], [None, max_value]],
        "loudness": [[None, min_value], [None, max_value]],
        "speechiness": [[None, min_value], [None, max_value]],
        "tempo": [[None, min_value], [None, max_value]],
        "time_signature": [[None, min_value], [None, max_value]],
        "valence": [[None, min_value], [None, max_value]],
        "duration_ms": [[None, min_value], [None, max_value]],
        "popularity": [[None, min_value], [None, max_value]],
    }

    for track_id, track in track_list.items():
        for key in return_object:
            if not track.__getattribute__(f"_{key}") is None and return_object[key][0][
                1
            ] > track.__getattribute__(f"_{key}"):
                return_object[key][0][1] = track.__getattribute__(f"_{key}")
                return_object[key][0][0] = track_id
            if not track.__getattribute__(f"_{key}") is None and return_object[key][1][
                1
            ] < track.__getattribute__(f"_{key}"):
                return_object[key][1][1] = track.__getattribute__(f"_{key}")
                return_object[key][1][0] = track_id

    return return_object


# @performance_timer
def find_average_audio_features(track_list: list[Track]) -> dict[str, float]:
    """Find the average value for a given key."""
    no_of_tracks = len(track_list)
    return_object = {
        "acousticness": 0.0,
        "danceability": 0.0,
        "energy": 0.0,
        "instrumentalness": 0.0,
        "liveness": 0.0,
        "loudness": 0.0,
        "speechiness": 0.0,
        "tempo": 0.0,
        "time_signature": 0.0,
        "valence": 0.0,
        "duration_ms": 0.0,
        "popularity": 0.0,
    }

    for _track_id, track in track_list.items():
        for key in return_object:
            if track.__getattribute__(f"_{key}") is None:
                continue
            return_object[key] += track.__getattribute__(f"_{key}")

    for key in return_object:
        if key == "duration_ms":
            return_object[key] = int(return_object[key] // no_of_tracks)
        else:
            return_object[key] = round(return_object[key] / no_of_tracks, 5)

    return return_object


def convert_key(key: int) -> str:
    """Convert key from pitch class notation to Str value.

    i.e: 0 = C, 1 - C♯/D♭ 2=D etc.
    """
    if key == -1:
        return "No Key found."
    key_list = [
        "C",
        "C♯/D♭",
        "D",
        "D♯/E♭",
        "E/F♭",
        "E♯/F",
        "F♯/G♭",
        "G",
        "G♯/A♭",
        "A",
        "A♯/B♭",
        "B",
    ]
    return key_list[key]


def convert_mode(mode: int) -> str:
    """Convert Mode from int to String."""
    if mode == 0:
        return "Minor"
    return "Major"


def convert_duration_ms(duration_ms: int) -> str:
    """Convert the value for duration ms to time format."""
    seconds = duration_ms // 1000
    minutes = seconds // 60
    remaining_seconds = seconds - (60 * minutes)
    if remaining_seconds < 10:
        remaining_seconds = f"0{remaining_seconds}"
    if minutes >= 60:
        hours = minutes // 60
        remaining_minutes = minutes - (60 * hours)
        if remaining_minutes < 10:
            remaining_minutes = f"0{remaining_minutes}"
        return f"{hours}:{remaining_minutes}:{remaining_seconds}"
    if minutes < 10:
        minutes = f"0{minutes}"
    return f"{minutes}:{remaining_seconds}"


def convert_time_signature(time_sig: str) -> str:
    """add the /4 to the time signature"""
    return f"{time_sig}/4"


def get_most_common_from_breakdown(breakdown: dict[str, int]) -> tuple[str, int]:
    """Take a breakdown dict and return the key value with the highest value."""
    max = float("-inf")
    max_key = None
    for key, value in breakdown.items():
        if max < value:
            max = value
            max_key = key
    return max_key, max
