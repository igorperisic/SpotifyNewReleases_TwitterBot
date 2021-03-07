 *detailed explanation of the NewSpotifyReleasesTweetBot.py*

The goal of this Python program is to send out tweets once a day for every artist that released an album/song on that day. 
First, the program extracts information from Spotfiy using Spotifys API and spotipy. It is only possible to extract at most the last fifty
new releases from Spotify. The only information this program needs are Artist_Name, Album_Name, Album_Cover, and Release_date. Artist_Name,
Album_Name and Release_date are all stored in a list, however the Album_Cover is downloaded as a jpeg file to a local PC. Once they are stored in a list,
the program compares todays date to Release_date for all fifty releases. If these two dates are equal to each other, a tweet gets sent out using Twitters API and tweepy.
Finally, once the program is finished it deletes all downloaded album covers. 

The tweet is sent out in this format: 

"
New Music Out Now:

Artist_Name - Album/Song_Name

     Album/Song_Cover
"
