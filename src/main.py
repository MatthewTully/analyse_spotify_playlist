"""Main entry for Application."""

"""
    Application flow:

        - Fetch auth token for future requests
        - Take spotify ids for the requested playlist. (how to provide ids? should be able to read from a file, or input with the cli)
        - Make a request for each id.
        - Create a class for the playlist
        - for each track create a class and make a request for the audio features (can do upto 100 tracks at a time)
        - then analyse data for the tracks and populate properties against the playlist.
        - Display the end results. 

    Things to consider:
        - Number of requests to spotify (try to minimise it as much as possible, use endpoints that allow several tracks in one request)
        - When analysing data, consider big O for the functions/methods. Can be dealing with hundreds of tracks at a time. 
        - If we want genre for the tracks, we need to get Artists. 
"""
from src.analyse import analyse_playlists


def main():
    """Start application."""
    analyse_playlists("5coU7FcTQl7fZmsUXBUHji")


if "__main__" in __name__:
    main()
