"""Main entry for Application."""

from analyse_spotify_playlist.analyse import analyse_playlists
from analyse_spotify_playlist.utils import performance_timer


@performance_timer
def main(playlist_ids: list[str], verbose: bool):
    """Start application."""
    for playlist_id in playlist_ids:
        analyse_playlists(playlist_id, verbose)
