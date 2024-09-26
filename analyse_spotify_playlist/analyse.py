"""Get Playlist information and analyse."""

from analyse_spotify_playlist.access_token import AccessToken
from analyse_spotify_playlist.file_output import FileOutput
from analyse_spotify_playlist.logger import Log
from analyse_spotify_playlist.outbound_requests import (
    pull_next_set_of_tracks,
    pull_playlist_data,
    pull_tracks_audio_features_r,
    request_access_token,
)
from analyse_spotify_playlist.playlist import Playlist
from analyse_spotify_playlist.utils import (
    clean_raw_playlist_data,
    clean_up_track_features,
    convert_duration_ms,
    convert_time_signature,
)

logger = Log()


def populate_track_features(playlist: Playlist, cleaned_feature_list: tuple) -> None:
    """Populate track in playlist with the audio features."""
    for id, track_feature in cleaned_feature_list:
        if id is None:
            continue
        playlist.get_track(id).populate_audio_features(**track_feature)


def analyse_playlists(playlist_id: str, depth: int) -> None:
    """Trigger the analysis."""
    file_handler = FileOutput()
    token = AccessToken(**request_access_token())
    raw_playlist = pull_playlist_data(token.get_token(), playlist_id)

    clean_playlist = clean_raw_playlist_data(raw_playlist)
    playlist = Playlist(**clean_playlist)
    if playlist.next_url:
        pull_next_set_of_tracks(token.get_token(), playlist)
    track_ids = playlist.get_all_track_ids()
    audio_features_list = pull_tracks_audio_features_r(token.get_token(), track_ids)
    cleaned_features = list(map(clean_up_track_features, audio_features_list))
    populate_track_features(playlist, cleaned_features)
    playlist.analyse_tracks_audio_feature()
    playlist.oldest_and_newest()
    if file_handler.write_to_file:
        file_handler.set_file_name(playlist.name)
        file_handler.create_file()
    output_analysis(playlist, depth, file_handler)


def output_analysis(playlist: Playlist, depth: int, file_handler: FileOutput) -> None:
    """Output Analysis details."""
    header = "----- PLAYLIST ANALYSIS -----\n"
    logger.print(header)
    file_handler.write(header)

    playlist_info = playlist_information(playlist)
    logger.print(playlist_info)
    file_handler.write(playlist_info)

    track_summary = playlist_track_summary(playlist)
    logger.print(track_summary)
    file_handler.write(track_summary)

    if depth > 0:
        in_depth = in_depth_breakdown(playlist)
        logger.print(in_depth)
        file_handler.write(in_depth)
    if depth > 1:
        raw_audio_features = audio_features_breakdown(playlist)
        logger.print(raw_audio_features)
        file_handler.write(raw_audio_features)
    footer = "-----------------------------"
    logger.print(footer)
    file_handler.write(footer)


def audio_features_breakdown(playlist: Playlist) -> None:
    """Print the min and max values for the audio features."""
    audio_breakdown = "\n--- RAW AUDIO FEATURES BREAKDOWN ---"

    keys = [
        "duration_ms",
        "acousticness",
        "danceability",
        "energy",
        "instrumentalness",
        "liveness",
        "loudness",
        "speechiness",
        "tempo",
        "time_signature",
        "valence",
        "popularity",
    ]
    min_max_list = playlist.min_max_analysis
    average_list = playlist.average_analysis
    for key in keys:
        audio_breakdown += f"\n\n{key.title().replace('_Ms', '').replace('_',' ')}:"
        min = min_max_list[key][0]
        min_track = playlist.get_track(min[0])
        max = min_max_list[key][1]
        max_track = playlist.get_track(max[0])
        to_add = ""
        if "duration" in key:
            to_add = f"""
Minimum: {convert_duration_ms(min[1])} Track: {min_track._name}, by {min_track._artists[0]['name']} (ID: {min[0]})
Maximum: {convert_duration_ms(max[1])} Track: {max_track._name}, by {max_track._artists[0]['name']} (ID: {max[0]})
Average: {convert_duration_ms(average_list[key])}"""
        elif "time_signature" == key:
            to_add = f"""
Minimum: {convert_time_signature(min[1])} Track: {min_track._name}, by {min_track._artists[0]['name']} (ID: {min[0]})
Maximum: {convert_time_signature(max[1])} Track: {max_track._name}, by {max_track._artists[0]['name']} (ID: {max[0]})
Average: {convert_time_signature(average_list[key])}"""
        else:
            to_add = f"""
Minimum: {(min[1])} Track: {min_track._name}, by {min_track._artists[0]['name']} (ID: {min[0]})
Maximum: {(max[1])} Track: {max_track._name}, by {max_track._artists[0]['name']} (ID: {max[0]})
Average: {(average_list[key])}"""
        audio_breakdown += to_add
    return audio_breakdown


def playlist_information(playlist: Playlist) -> str:
    """Return standard playlist information."""
    return f"""Playlist: {playlist.name}
Description: {playlist.description}
Followers: {playlist.followers}
Total Tracks: {playlist.total_tracks}
Owner: {playlist.owner}
Collaborative: {playlist.collaborative}
Playlist Type: {playlist.get_playlist_visibility()}

"""


def playlist_track_summary(playlist: Playlist) -> str:
    """Return a summary of the tracks info."""
    track_summary = f"""--- TRACK SUMMARY ---
Total Playable Tracks: {len(playlist._tracks)}
Total Tracks marked as Explicit: {playlist.total_explicit_tracks()} ({round(playlist.total_explicit_tracks()/len(playlist._tracks) * 100, 2)}%)

Oldest Track: "{playlist.oldest_track._name}", by {playlist.oldest_track._artists[0]['name']}, Released: {playlist.oldest_track.get_release_date()}
Newest Track: "{playlist.newest_track._name}", by {playlist.newest_track._artists[0]['name']}, Released: {playlist.newest_track.get_release_date()}
"""
    min_max_list = playlist.min_max_analysis
    average_list = playlist.average_analysis

    min_duration = min_max_list["duration_ms"][0]
    min_duration_track = playlist.get_track(min_duration[0])
    max_duration = min_max_list["duration_ms"][1]
    max_duration_track = playlist.get_track(max_duration[0])

    track_summary += f"""
The Shortest Track in the playlist is: \"{min_duration_track._name}\", by {min_duration_track._artists[0]['name']} with a runtime of {convert_duration_ms(min_duration[1])}
The Longest Track in the playlist is: \"{max_duration_track._name}\", by {max_duration_track._artists[0]['name']} with a runtime of {convert_duration_ms(max_duration[1])}
The Average Track duration is: {convert_duration_ms(average_list['duration_ms'])}

Most Tracks Are from the {playlist.get_most_common_decade()[0]}'s ({round(playlist.get_most_common_decade()[1]/len(playlist._tracks) * 100, 2)}%)
Most Tracks Are from the {playlist.get_most_common_album_type()[0].title()} Release ({round(playlist.get_most_common_album_type()[1]/len(playlist._tracks) * 100, 2)}%)

The Most Common Key is: {playlist.get_most_common_key()[0]} ({round(playlist.get_most_common_key()[1]/len(playlist._tracks) * 100, 2)}%)
The Most Common Mode is: {playlist.get_most_common_mode()[0]} ({round(playlist.get_most_common_mode()[1]/len(playlist._tracks) * 100, 2)}%)
The Most Common Time Signature is: {convert_time_signature(playlist.get_most_common_time_signature()[0])} ({round(playlist.get_most_common_time_signature()[1]/len(playlist._tracks) * 100, 2)}%)
"""
    min_loudness = min_max_list["loudness"][0]
    min_loudness_track = playlist.get_track(min_loudness[0])
    max_loudness = min_max_list["loudness"][1]
    max_loudness_track = playlist.get_track(max_loudness[0])

    track_summary += f"""
The Quietest Track in the playlist is: \"{min_loudness_track._name}\", by {min_loudness_track._artists[0]['name']} with {min_loudness[1]} dB
The Loudest Track in the playlist is: \"{max_loudness_track._name}\", by {max_loudness_track._artists[0]['name']} with {max_loudness[1]} dB
The Average dB is: {round(average_list['loudness'],2)} dB
"""

    min_tempo = min_max_list["tempo"][0]
    min_tempo_track = playlist.get_track(min_tempo[0])
    max_tempo = min_max_list["tempo"][1]
    max_tempo_track = playlist.get_track(max_tempo[0])
    track_summary += f"""
The Track with the lowest tempo is: \"{min_tempo_track._name}\", by {min_tempo_track._artists[0]['name']} with a {min_tempo[1]} BPM
The Track with the highest tempo is: \"{max_tempo_track._name}\", by {max_tempo_track._artists[0]['name']} with {max_tempo[1]} BPM
The Average Tempo is: {round(average_list['tempo'],2)} BPM
"""
    average_valence = average_list["valence"]
    desc = None
    if average_valence > 0.66:
        desc = "Positive. The Valence of the playlist is high, and the majority of tracks could be described as Happy, Cheerful, or Euphoric"
    elif average_valence < 0.33:
        desc = "Negative. The Valence of the playlist is low, and the majority of tracks could be described as Sad, Depressed, or Angry"
    else:
        desc = "Mixed. The Valence of the playlist is in the middle ground, and the tracks are likely a mix of both positive and negative."

    min_valence = min_max_list["valence"][0]
    min_valence_track = playlist.get_track(min_valence[0])
    max_valence = min_max_list["valence"][1]
    max_valence_track = playlist.get_track(max_valence[0])

    track_summary += f"""
The Vibe of the playlist is {desc}
The Least Positive Track in the playlist is: \"{min_valence_track._name}\", by {min_valence_track._artists[0]['name']} with a Valence score of {round(min_valence[1] * 100,2)}%
The Most Positive Track in the playlist is: \"{max_valence_track._name}\", by {max_valence_track._artists[0]['name']} with a Valence score of {round(max_valence[1] * 100, 2)}%
"""

    average_danceability = average_list["danceability"]
    desc = None
    if average_danceability > 0.66:
        desc = "This playlist has a High danceability score. You can boogie to this playlist"
    elif average_danceability < 0.33:
        desc = "This playlist has a Low danceability score. You're gonna have a hard time dancing to this"
    else:
        desc = "This playlist has a Mid danceability score. You can dance to some of tracks on this playlist, still, wouldn't recommend it for the local disco night"

    min_danceability = min_max_list["danceability"][0]
    min_danceability_track = playlist.get_track(min_danceability[0])
    max_danceability = min_max_list["danceability"][1]
    max_danceability_track = playlist.get_track(max_danceability[0])

    track_summary += f"""
{desc}.
The Least Danceable Track in the playlist is: \"{min_danceability_track._name}\", by {min_danceability_track._artists[0]['name']} with a danceability score of {round(min_danceability[1] * 100,2)}%
The Most Danceable Track in the playlist is: \"{max_danceability_track._name}\", by {max_danceability_track._artists[0]['name']} with a danceability score of {round(max_danceability[1] * 100, 2)}%
"""
    average_energy = average_list["energy"]
    desc = None
    if average_energy > 0.66:
        desc = "The Energy of the playlist is High, might be good to use while going for a run... No promises"
    elif average_energy < 0.33:
        desc = "The Energy of the playlist is Low, could be good to relax, sleep or study to"
    else:
        desc = "The Energy of the playlist is Mid, could contain a mix of high and low energy tracks"

    min_energy = min_max_list["energy"][0]
    min_energy_track = playlist.get_track(min_energy[0])
    max_energy = min_max_list["energy"][1]
    max_energy_track = playlist.get_track(max_energy[0])
    track_summary += f"""
{desc}.
The Lowest Energy Track in the playlist is: \"{min_energy_track._name}\", by {min_energy_track._artists[0]['name']} with a energy score of {round(min_energy[1] * 100,2)}%
The Highest Energy Track in the playlist is: \"{max_energy_track._name}\", by {max_energy_track._artists[0]['name']} with a energy score of {round(max_energy[1] * 100, 2)}%

The playlist contains {playlist.total_instrumental_tracks()} Instrumental tracks *
The playlist contains {playlist.total_spoken_word_tracks()} Spoken Word tracks *

The Most Popular Tracks in the playlist (according to spotify):
"""
    most_popular = playlist.get_most_popular_list()
    for i in range(len(most_popular)):
        if i + 1 < 10:
            track_summary += f"\n {i+1}.  {most_popular[i]._name} - {most_popular[i]._artists[0]['name']} ({most_popular[i]._popularity})"
        else:
            track_summary += f"\n{i+1}.  {most_popular[i]._name} - {most_popular[i]._artists[0]['name']} ({most_popular[i]._popularity})"

    track_summary += (
        f"\n\nThe Least Popular Tracks in the playlist (according to spotify) **:"
    )
    least_popular = playlist.get_least_popular_list()
    for i in range(len(least_popular)):
        if i + 1 < 10:
            track_summary += f"\n {i+1}.  {least_popular[i]._name} - {least_popular[i]._artists[0]['name']} ({least_popular[i]._popularity})"
        else:
            track_summary += f"\n{i+1}.  {least_popular[i]._name} - {least_popular[i]._artists[0]['name']} ({least_popular[i]._popularity})"
    track_summary += """

*  Allegedly.
** If all have a score of zero, then list is in order of added to playlist.
"""
    return track_summary


def in_depth_breakdown(playlist: Playlist) -> None:
    """Print an in depth breakdown of the tracks."""
    in_depth = f"""--- IN DEPTH BREAKDOWNS ---

 Album Type Breakdown:"""
    breakdown = playlist.get_album_type_breakdown()
    for key, value in breakdown.items():
        in_depth += f"\n  {key.title()}: {value}"
    in_depth += "\n\n Decade Release Breakdown:"
    breakdown = playlist.get_track_decade_release_breakdown()
    for key, value in breakdown.items():
        in_depth += f"\n  {key}: {value}"
    in_depth += "\n\n Key Breakdown:"
    breakdown = playlist.get_key_breakdown()
    for key, value in breakdown.items():
        in_depth += f"\n  {key}: {value}"
    in_depth += "\n\n Mode Breakdown:"
    breakdown = playlist.get_mode_breakdown()
    for key, value in breakdown.items():
        in_depth += f"\n  {key}: {value}"
    in_depth += "\n\n Time Signature Breakdown:"
    breakdown = playlist.get_time_signature_breakdown()
    for key, value in breakdown.items():
        in_depth += f"\n  {convert_time_signature(key)}: {value}"
    if playlist.total_instrumental_tracks() > 0:
        in_depth += "\n\nInstrumental Tracks: (*Spotify's instrumental score if often way off. Chances are half the tracks below won't be instrumental.)"
        for track in playlist.get_instrumental_tracks():
            in_depth += f"\n  {track._name} - {track._artists[0]['name']}   (Instrumentalness score: {track._instrumentalness})"
    if playlist.total_spoken_word_tracks() > 0:
        in_depth += "\n\nSpoken Word Tracks:"
        for track in playlist.get_spoken_word_tracks():
            in_depth += f"\n  {track._name} - {track._artists[0]['name']}   (Speechiness score: {track._speechiness})"
    return in_depth
