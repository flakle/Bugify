import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import time
import datetime
import gspread
import os

SPOTIPY_CLIENT_ID = '047ae1176d0449f4a07ac31d69d56317'
SPOTIPY_CLIENT_SECRET = '2be75abb718248a6949704751c9288e6'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:9090'
SCOPE = "user-top-read"

sp = spotipy.Spotify (auth_manager=SpotifyOAuth (client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=SCOPE))

results = sp.current_user_top_tracks()

top_tracks_short = sp.current_user_top_tracks (limit=5, offset=0, time_range="short_term")

type(top_tracks_short)

def get_track_ids(time_frame):
    track_ids = []
    for song in time_frame ['items'] :
        track_ids.append(song['id'])
    return track_ids

track_ids = get_track_ids(top_tracks_short)

def get_track_features (id):
    meta = sp.track(id)
    name = meta['name']
    artist = meta['album']['artists'][0]['name']
    spotify_url = meta['external_urls']['spotify']
    track_info = [name, artist, spotify_url,]
    return track_info

time_ranges = ["short_term", "medium_term", "long_term"]

tracks = []
for i in range(len(track_ids)):
    time.sleep(.5)
    track = get_track_features(track_ids [i])
    track.append(track)

df = pd.DataFrame(tracks, columns = ['name', 'album', 'artist', 'spotify_url', 'album_cover'])
df.head(5)

def insert_to_gsheet(track_ids, time_period):
    tracks = []
    for i in range(len(track_ids)):
        time.sleep(.5)
        track = get_track_features(track_ids[i])
        tracks.append(track)
    df = pd.DataFrame(tracks, columns = ['name', 'artist', 'spotify_url'])
    gc = gspread.service_account(filename='C:\\Users\\tarar\\OneDrive\\Documents\\Software\\Bugify\\Service-Account-Key-Bugify.json') 
    sh = gc.open('Bugify')
    worksheet = sh.worksheet(f'{time_period}')
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    return tracks

for time_period in time_ranges:
    top_tracks = sp.current_user_top_tracks(limit=5, offset=0, time_range=time_period)
    track_ids = get_track_ids(top_tracks)
    insert_to_gsheet(track_ids, time_period)
    print("Done")

    