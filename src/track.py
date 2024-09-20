"""Class definition for Track data."""


class Track:
    """Track in a playlist."""

    def __init__(
        self,
        album: dict,
        artists: dict,
        available_markets: list[str],
        disc_number: int,
        duration_ms: int,
        explicit: bool,
        external_ids: dict,
        external_urls: dict,
        href: str,
        id: str,
        name: str,
        popularity: int,
        preview_url: str,
        track_number: int,
        type: str,
        uri: str,
        is_local: bool,
        episode: bool,
        track: bool,
    ) -> None:
        self._album = album
        self._artists = artists
        self._available_markets = available_markets
        self._disc_number = disc_number
        self._duration_ms = duration_ms
        self._explicit = explicit
        self._external_ids = external_ids
        self._external_urls = external_urls
        self._href = href
        self._id = id
        self._name = name
        self._popularity = popularity
        self._preview_url = preview_url
        self._track_number = track_number
        self._type = type
        self._uri = uri
        self._is_local = is_local
        self._episode = episode
        self._track = track

        # Features to fetch
        self._acousticness = None
        self._danceability = None
        self._energy = None
        self._instrumentalness = None
        self._key = None
        self._liveness = None
        self._loudness = None
        self._mode = None
        self._speechiness = None
        self._tempo = None
        self._time_signature = None
        self._valence = None

    def populate_audio_features(
        self,
        acousticness: float,
        danceability: float,
        energy: float,
        instrumentalness: float,
        key: int,
        liveness: float,
        loudness: float,
        mode: int,
        speechiness: float,
        tempo: float,
        time_signature: int,
        valence: float,
    ) -> None:
        """Populate the track with the extra data from the Get audio features endpoint."""
        self._acousticness = acousticness
        self._danceability = danceability
        self._energy = energy
        self._instrumentalness = instrumentalness
        self._key = key
        self._liveness = liveness
        self._loudness = loudness
        self._mode = mode
        self._speechiness = speechiness
        self._tempo = tempo
        self._time_signature = time_signature
        self._valence = valence
