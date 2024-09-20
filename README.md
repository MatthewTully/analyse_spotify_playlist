# Music Playlist Analyser

## About

Uses the Spotify API to pull data about  Spotify playlists, and then analyses the tracks to provide an in-depth look at the playlist. Can be used to compare multiple playlists together.

The following information can be found for individual Tracks:

* Acousticness
* Duration
* Energy
* Instrumentalness
* Key
* Liveness (likelihood the track was a live performance)
* Loudness (db)
* Mode
* Speechiness
* Tempo
* Time Signature
* Valence
* Popularity of the Track (on spotify's platform)

From the above, the following can be determined for the playlists:

* An Average for each of the track specific information. For example: Key, Valence, or time signature
* Most common Genre
* Longest and shortest track
* Most and least popular track (on spotify)
* "Hipness" (i.e what is the average popularity and release date of the tracks in the playlist. Is it full of obscure tracks, the newest most popular tracks, or Golden oldies that have stayed popular, etc.)
* Oldest, and newest track (release date of the track could be incorrect if from a re-release)
* Average decade for the tracks (i.e In a playlist of 10 songs, 7 are from the 1990's, so the average decade would be 90s.)

*N.B The data on the tracks is from Spotify. I do not know how this data is determined, and I cannot vouch for the accuracy. The data often comes with a confidence score and where possible, only tracks with a hight confidence rating is used for the analysis.*

## To install
TODO

## To run
TODO

## Example output
TODO

### Useful Links 
* [text](https://developer.spotify.com/dashboard/0fa880e66fc74f66b4a6e5baab19fad2)
* [text](https://developer.spotify.com/documentation/web-api)
* [text](https://developer.spotify.com/)