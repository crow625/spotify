#December 15 2021

import numpy as np
import pandas as pd
import seaborn as sns
import time
import ast
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

from secret_ids import *

DEFAULT_CHAR = '?'
uid = "rhdmobgokunyivwk2uhph47na" #my user ID
ptv = "spotify:artist:4iJLPqClelZOBCBifm8Fzv" #Pierce the Veil artist ID
scope = "user-library-read user-read-currently-playing"
redirect_uri='http://localhost:8888/callback/'

client_credentials_manager = SpotifyClientCredentials(client_id=clientID, client_secret=clientSecret)
oauth = SpotifyOAuth(scope=scope, client_id=clientID, client_secret=clientSecret, redirect_uri=redirect_uri)

token = spotipy.util.prompt_for_user_token(username=uid,
                                               scope=scope,
                                               client_id=clientID,
                                               client_secret=clientSecret,
                                               redirect_uri=redirect_uri)
if token:
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, auth_manager=oauth, auth=token)
else:
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, auth_manager=oauth)
    
'''
Handle any characters in a string that the IDE cannot display.
Returns a string with any invalid characters replaced by default.
    string: string. The string to parse.
    default: char. The sequence to replace invalid chars with.
'''
def manage_unicode(string, default):
    string = list(string)
    for i in range(len(string)):
        if ord(string[i]) > 65535:
            string[i] = default
    return "".join(string)

'''
Returns a list of every album by an artist.
    spotify: spotipy Spotify object.
    artist_id: string. The artist's spotify ID.
'''
def get_artist_albums(spotify, artist_id):
    returns = []
    results = spotify.artist_albums(artist_id, album_type='album')
    albums = results['items']
    for album in albums:
        returns.append(album['name'])
        
    return returns

''' Returns a string with the given track's artist and title.
    track: Spotify track
'''
def format_track(track):
    return track['artists'][0]['name'] + " - " + track['name']

''' Returns the song listed at offset from the current user's library.
    spotify: spotipy Spotify object
    offset: int. desired index of song
'''
def get_user_song(spotify, offset):
    results = spotify.current_user_saved_tracks(limit=1, offset=offset)
    return results['items'][0]['track']

''' Saves limit number of a user's liked songs to a csv file called "liked_songs.csv".
    Also saves the date it was added.
        spotify: spotipy Spotify object
        limit: int. number of songs to get, starting from most recently added
'''
def save_liked_songs(spotify, limit):
    tracks = []
    for i in range(0, limit, 20):
        results = spotify.current_user_saved_tracks(limit=20, offset=i)
        for track in results['items']:
            buf = track['track']
            buf['added_at'] = track['added_at']
            tracks.append(buf)
            
        time.sleep(1)
            
    df = pd.DataFrame(data=tracks)
    df.to_csv("liked_songs.csv", index=False)
    
def ms_to_min(n):
    sec = int(n//1000)
    minutes = sec//60
    sec -= minutes*60
    return str(minutes) + ":" + str(f'{sec:02d}')

def remove_dupes(x):
    return list(dict.fromkeys(x))

def main():
    #df = pd.read_csv("liked_songs.csv", converters = {'album':ast.literal_eval, 'artists':ast.literal_eval})
    #df = pd.read_csv("liked_songs.csv")
    #print(df["name"].value_counts().sort_values())
    print(get_artist_albums(sp, ptv))
        
        
if __name__ == "__main__":
    main()