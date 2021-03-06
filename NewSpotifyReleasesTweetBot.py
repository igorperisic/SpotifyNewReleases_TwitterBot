#Igor Perisic

import tweepy
import time
import os
import requests
import spotipy
import json
import collections as co
from spotipy.oauth2 import SpotifyClientCredentials
from operator import attrgetter
from datetime import date

#twitter
consumer_key = ""           #insert own consumer_key
consumer_secret = ""        #insert own consumer_secret
access_token = ""           #insert own access_token
access_token_secret = ""    #insert own access_token_secret

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#spotify 
client_id = ""               #insert own client_id
client_secret = ""           #insert own client_se

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id, client_secret))

#downloads album cover to local PC from url
def download_album_cover(url):
    download_path = os.getcwd() + os.sep + url.rsplit('/', 1)[-1] 
    r = requests.get(url, stream = True) 
    if r.status_code == 200: 
        with open(download_path, 'wb') as f: 
            for chunk in r.iter_content(1024): 
                f.write(chunk) 
        return download_path 

releases = spotify.new_releases(limit = 50) #50 new releases from spotify
albums = releases['albums']['items']

Album = co.namedtuple(typename = 'Album', field_names = ['album_name',
                                                         'artist_name',
                                                         'release_date',
                                                         'album_cover'])

newReleases = []

for album in albums:
    album_cover = download_album_cover(album['images'][0]['url'])
    artist_sublist = []
    for artist in album['artists']:
        artist_sublist.append(artist['name'])
    newReleases.append(Album(album_name = album['name'],
                              artist_name = artist_sublist,
                              release_date = album['release_date'],
                              album_cover = album_cover))

currentDate = date.today()
today = currentDate.strftime("%Y-%m-%d")    #set date to a string for comparison 

i = 0
while i < len(newReleases):
    releaseDate = list(map(attrgetter('release_date'), newReleases))    #extracts release_date attribute  
    albumCover = list(map(attrgetter('album_cover'), newReleases))      #extracts album_cover attribute  

    #AlbumCover list to string 
    albumCoverStr = ""           
    for x in albumCover[i]:        
        albumCoverStr += x  

    if releaseDate[i] == today:    #checks if Spotifys "New Releases" were released on the current day
        
        albumName = list(map(attrgetter('album_name'), newReleases))    #extracts album_name attribute 
        artistName = list(map(attrgetter('artist_name'), newReleases))  #extracts artist_name attribute            
        
        imagePath = api.media_upload(albumCoverStr) 

        #ArtistName list to string 
        ArtistsOnSong = len(artistName[i]) #people per album/song        
        artistNameStr = "" 
        count = 0        
        for x in artistName[i]:
            count += 1
            for y in x:
                artistNameStr += y 
            if count < ArtistsOnSong:
                artistNameStr += ", "                

        #AlbumName list to string 
        albumNameStr = ""  
        for x in albumName[i]:
            albumNameStr += x

        tweet = "New music out now:\n\n" + artistNameStr + " - " + albumNameStr

        api.update_status(status = tweet, media_ids = [imagePath.media_id])     #uploads tweet with text and image
        
    os.remove(albumCoverStr)    #deletes album covers from local pc
    i += 1