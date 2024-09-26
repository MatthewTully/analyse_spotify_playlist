# Music Playlist Analyser

## About

Uses the Spotify API to pull data about  Spotify playlists, and then analyses the tracks to provide an in-depth look at the playlist. Can be used to analyse multiple playlists.

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
* ~~Most common Genre~~ Genre is only returned with the Artist. We could look at pulling artist info per track, but that will be a lot of requests for larger playlist. The information will likely be inaccurate as the genre of the artist might not necessarily match the genre of the track (Think Childish Gambino, whose genre would be likely be Hip Hop. Any track on their album "Awaken, My love!" would not fit this genre, and would be better described as R&B). 
* Longest and shortest track
* Most and least popular track (on spotify)
* Oldest, and newest track (release date of the track could be incorrect if from a re-release)
* Average decade for the tracks (i.e In a playlist of 10 songs, 7 are from the 1990's, so the average decade would be 90s.)

*N.B The data on the tracks is from Spotify. I do not know how this data is determined, and I cannot vouch for the accuracy. The data often comes with a confidence score and where possible, only tracks with a hight confidence rating is used for the analysis.*

## To install
Pull the repo and run:
```pip install .```
from the directory.

Open the file config.py and populate the `CLIENT_ID` and `CLIENT_SECRET` values. You can create an application with Spotify to get these values.
[Spotify Developer](https://developer.spotify.com/)

## To run
To run the application use `python -m analyse_spotify_playlist <playlist id> -v` replacing <playlist id> with the Id of the playlist you want to analyse. As it contains the -v flag it will print the result to the console. Multiple playlists can be analysed by splitting them by a comma (no spaces). 

You can use `-v` flag to output the result to the console. 

You can provide an `-o` flag and provide a file path to output the result. This will create a txt file. 

(At least one of `-v` or `-o` needs to be specified. Otherwise it will exit.)

You can specify the "depth" of the analyse with `-d` flag. This should be followed by an int from 0 to 2. For example `-d 1`

>depth levels:
> - 0 - default, outputs the summary
> - 1 - In depth breakdowns, output the summary and some more in depth break downs, such as how many tracks are in what key.
> - 2 - Audio Feature data, outputs the above, plus the max, min, and average for audio feature data. 

## How to find the playlist Id
To find the Spotify playlist id enter the playlist page, click the (...) button near the play button, go down to "Share" and click "Copy link to playlist". Paste the link anywhere, The playlist id is the string right after playlist/ and before the ?si.

>i.e `https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M?si=638f2ae5f14448e0`
>
> Playlist id = 37i9dQZF1DXcBWIGoYBM5M

## Example output
[Example Output](docs/Today’s_Top_Hits_analysis.txt)
