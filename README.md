# 2024_guess_the_song_game
Script that takes a link to a Spotify playlist and generates printable pages with cards that can be used to guess the song name, artist, and release year. Idea from the game Hitster. 

I got the game Hitster as a Christmas gift. I liked playing the game but ran out of playing cards fast. The game involves listening to songs and guessing what year they were released compared to some other years. 

This script takes any Spotify playlist and generates an A4 pdf document with scannable Spotify codes and information text (track name, artists, and release year). Every other page is covered by codes and text so that it can be printed on both sides and then cut into cards. I have tried it and it works well. 

What you need to do: 
- Get a Spotify Web API (instructions are on the internet)
- Get a link to your desired playlist
- Install some fairly uncommon Spotify libraries
- Plug it in and try to read my messy code

Known limitations: 
- Spotify sometimes has a track on multiple albums. The release date associated with a track in a playlist is the album release date. Sometimes, remastered Spotify tracks or old tracks are put on albums that actually are too recent. Unfortunately, I cannot find a way to check this that does not involve manually going through every track. Perhaps someone can improve this by searching some other track database or something. But it works well for recent tracks.

If you use this, have fun :)

2024-12-25
