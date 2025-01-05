# 2024_guess_the_song_game
This script takes any Spotify playlist and generates an A4 pdf document with scannable Spotify codes and information text (track name, artists, and release year). Every other page is covered by codes and text so that it can be printed on both sides and then cut into cards. I have tried it and it works well. 

The idea is from the game Hitster. I got Hitster as a Christmas gift and liked playing the game, but ran out of playing cards fast. The game involves listening to songs and guessing what year they were released compared to some other years. 

What you need to do: 
- Get a Spotify Web API (https://developer.spotify.com/documentation/web-api)
- Get a link to your desired playlist
- Install some Python libraries
- Plug it in and try to read my messy code

Known limitations: 
- Spotify sometimes has a track on multiple albums. The release date associated with a track in a playlist is the album release date. Sometimes, remastered Spotify tracks or old tracks are put on albums that are too recent. Unfortunately, I cannot find a way to fix this that does not involve manually going through every track. Perhaps this could be fixed by searching some other track database for the earliest release of each track. But it works well for recent tracks. 

2024-12-25
