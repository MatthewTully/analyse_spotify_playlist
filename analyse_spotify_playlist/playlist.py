"""Class definition for the Playlist data."""

from copy import deepcopy

from analyse_spotify_playlist.track import Track
from analyse_spotify_playlist.utils import (
    find_average_audio_features,
    find_min_max_audio_features,
    get_most_common_from_breakdown,
    performance_timer,
)


class Playlist:
    """Spotify Playlist."""

    def __init__(
        self,
        name: str,
        owner: dict,
        collaborative: bool,
        description: str,
        followers: dict,
        id: str,
        public: bool,
        tracks: dict,
    ) -> None:
        """Playlist Constructor."""
        self.id = id
        self.name = name
        self.owner = "Unknown"
        self.collaborative = "No"
        self.description = description
        self.followers = followers.get("total", 0)
        self.public = public
        self.total_tracks = tracks.get("total", 0)
        self._tracks: dict[str, Track] = {}
        self.next_url = None
        self.min_max_analysis = None
        self.average_analysis = None
        self.oldest_track = None
        self.newest_track = None
        self.album_type_breakdown = None
        self.decade_release_breakdown = None
        self.key_breakdown = None
        self.mode_breakdown = None
        self.time_signature_breakdown = None
        self.instrumental_tracks = None
        self.spoken_word_tracks = None

        if owner.get("display_name"):
            self.owner = owner.get("display_name")

        if collaborative:
            self.collaborative = "Yes"

        if tracks.get("items", None):
            self.add_tracks(tracks)

    def get_track(self, track_id: str) -> Track | None:
        """Return track id if it exists."""
        if not isinstance(track_id, str) or track_id == "":
            return None
        return self._tracks.get(track_id, None)

    def get_all_track_ids(self) -> list:
        """Return all ids for the tracks. Returns None if empty."""
        id_list = []
        if len(self._tracks) > 0:
            id_list = list(self._tracks.keys())
        return id_list

    def add_tracks(self, tracks: dict) -> None:
        """Populate the tracks list."""
        for track in tracks.get("items", []):
            if track["track"]["name"] in (None, ""):
                continue
            self._tracks[track["track"]["id"]] = Track(**track["track"])
        self.next_url = tracks.get("next", None)

    def analyse_tracks_audio_feature(self) -> None:
        """Find the min, max, and average for audio features."""
        self.min_max_analysis = find_min_max_audio_features(self._tracks)
        self.average_analysis = find_average_audio_features(self._tracks)

    def total_explicit_tracks(self) -> int:
        """Return the total number of explicit tracks in playlist."""
        explicit = 0
        for _id, track in self._tracks.items():
            if track._explicit:
                explicit += 1
        return explicit

    def get_album_type_breakdown(self) -> dict:
        """Breakdown album type for each track.

        i.e Single, Compilation, Album
        """
        if self.album_type_breakdown is None:
            self.album_type_breakdown = {"album": 0, "single": 0, "compilation": 0}
            for _id, track in self._tracks.items():
                self.album_type_breakdown[track.get_album_type()] += 1
        return self.album_type_breakdown

    def oldest_and_newest(self) -> None:
        """Return the oldest track (by release date) in the playlist."""

        def sort_by_date(track_tuple: tuple[str, Track]):
            return track_tuple[1].get_release_date()

        sorted_tracks = sorted(deepcopy(self._tracks).items(), key=sort_by_date)
        self.oldest_track = sorted_tracks[0][1]
        self.newest_track = sorted_tracks[-1][1]

    def get_track_decade_release_breakdown(self) -> dict:
        """Breakdown decade release for tracks."""
        if self.decade_release_breakdown is None:
            self.decade_release_breakdown = {}
            track_list = deepcopy(self._tracks).items()
            for track_id, track in track_list:
                year_released = track.get_release_date()[0:4]
                decade = f"{year_released[0:3]}0"
                if not decade in self.decade_release_breakdown:
                    self.decade_release_breakdown[decade] = 1
                else:
                    self.decade_release_breakdown[decade] += 1
        return dict(sorted(self.decade_release_breakdown.items()))

    def get_key_breakdown(self) -> dict:
        """Breakdown of the track Keys."""
        if self.key_breakdown is None:
            self.key_breakdown = {
                "C": 0,
                "C♯/D♭": 0,
                "D": 0,
                "D♯/E♭": 0,
                "E/F♭": 0,
                "E♯/F": 0,
                "F♯/G♭": 0,
                "G": 0,
                "G♯/A♭": 0,
                "A": 0,
                "A♯/B♭": 0,
                "B": 0,
            }

            for _id, track in self._tracks.items():
                if track._key:
                    self.key_breakdown[track._key] += 1
        return self.key_breakdown

    def get_mode_breakdown(self) -> dict:
        """Breakdown of the track mode."""
        if self.mode_breakdown is None:
            self.mode_breakdown = {"Minor": 0, "Major": 0}
            for _id, track in self._tracks.items():
                if track._mode:
                    self.mode_breakdown[track._mode] += 1
        return self.mode_breakdown

    def get_time_signature_breakdown(self) -> dict:
        """Breakdown of the track Time Signature."""
        if self.time_signature_breakdown is None:
            self.time_signature_breakdown = {}
            for track_id, track in self._tracks.items():
                if track._time_signature is None:
                    continue
                if not track._time_signature in self.time_signature_breakdown:
                    self.time_signature_breakdown[track._time_signature] = 1
                else:
                    self.time_signature_breakdown[track._time_signature] += 1
        return self.time_signature_breakdown

    def get_most_common_decade(self) -> tuple[str, int]:
        """Return the most common decade for tracks in playlist."""
        if self.decade_release_breakdown is None:
            self.get_track_decade_release_breakdown()
        return get_most_common_from_breakdown(self.decade_release_breakdown)

    def get_most_common_album_type(self) -> tuple[str, int]:
        """Return the most common album type."""
        if self.album_type_breakdown is None:
            self.get_album_type_breakdown()
        return get_most_common_from_breakdown(self.album_type_breakdown)

    def get_most_common_key(self) -> tuple[str, int]:
        """Return the most common key in the playlist."""
        if self.key_breakdown is None:
            self.get_key_breakdown()
        return get_most_common_from_breakdown(self.key_breakdown)

    def get_most_common_mode(self) -> tuple[str, int]:
        """Return the most common mode in the playlist."""
        if self.mode_breakdown is None:
            self.get_mode_breakdown()
        return get_most_common_from_breakdown(self.mode_breakdown)

    def get_most_common_time_signature(self) -> tuple[str, int]:
        """Return the most common time signature in the playlist."""
        if self.time_signature_breakdown is None:
            self.get_time_signature_breakdown()
        return get_most_common_from_breakdown(self.time_signature_breakdown)

    def get_playlist_visibility(self) -> str:
        """Return string Public / Private based on playlist."""
        if self.public:
            return "Public"
        return "Private"

    @staticmethod
    def __sort_by_popularity(track_tuple: tuple[str, Track]):
        return track_tuple[1]._popularity

    def get_most_popular_list(self) -> list:
        """Return most popular tracks in the playlist."""
        list_size = 10
        if len(self._tracks) < list_size:
            list_size = len(self._tracks)
        tracks_copy = deepcopy(self._tracks).items()

        sorted_list = sorted(tracks_copy, key=self.__sort_by_popularity, reverse=True)
        to_return = []
        for i in range(list_size):
            to_return.append(sorted_list[i][1])

        return to_return

    def get_least_popular_list(self) -> list:
        """Return least popular tracks in the playlist."""
        list_size = 10
        if len(self._tracks) < list_size:
            list_size = len(self._tracks)
        tracks_copy = deepcopy(self._tracks).items()

        sorted_list = sorted(tracks_copy, key=self.__sort_by_popularity, reverse=False)
        to_return = []
        for i in range(list_size):
            to_return.append(sorted_list[i][1])

        return to_return

    def get_instrumental_tracks(self) -> list:
        """Populate list with instrumental tracks."""
        # Spotify considers a track instrumental if the score is over 0.5
        if self.instrumental_tracks is None:
            self.instrumental_tracks = []
            for _track_id, track in self._tracks.items():
                if track._instrumentalness is None:
                    continue
                if track._instrumentalness >= 0.5:
                    self.instrumental_tracks.append(track)
        return self.instrumental_tracks

    def total_instrumental_tracks(self) -> int:
        """Return sum of instrumental tracks."""
        if self.instrumental_tracks is None:
            self.get_instrumental_tracks()
        return len(self.instrumental_tracks)

    def get_spoken_word_tracks(self) -> list:
        """Populate list with spoken word tracks."""
        # Spotify considers a track spoken word if the score is over 0.66
        if self.spoken_word_tracks is None:
            self.spoken_word_tracks = []
            for _track_id, track in self._tracks.items():
                if track._speechiness is None:
                    continue
                if track._speechiness >= 0.66:
                    self.spoken_word_tracks.append(track)
        return self.spoken_word_tracks

    def total_spoken_word_tracks(self) -> int:
        """Return sum of spoken_word tracks."""
        if self.spoken_word_tracks is None:
            self.get_spoken_word_tracks()
        return len(self.spoken_word_tracks)
