"""Class definition for the Playlist data."""

from src.track import Track


class Playlist:
    """Spotify Playlist."""

    def __init__(
        self,
        name: str,
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
        self.collaborative = collaborative
        self.description = description
        self.followers = followers.get("total", 0)
        self.public = public

        self.total_tracks = tracks.get("total", 0)
        self._tracks: dict[str, Track] = {}
        for track in tracks.get("items", []):
            self._tracks[track["track"]["id"]] = Track(**track["track"])

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
