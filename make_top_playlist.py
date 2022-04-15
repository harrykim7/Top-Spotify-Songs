import os
import pandas as pd
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

#client data from spotify dev for this app 
client_ID = '63ab47dce765482480375e7708b13092'
client_Secret = '0a68a8c15ee14d9baa842e1051f815b3'

#using spotipy, authenticating
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id = client_ID,
    client_secret= client_Secret,
    scope=  ["user-top-read","playlist-modify-private","playlist-modify-public"],
    redirect_uri = 'http://localhost:8000'))

#It will redirect you to a webpage to authenticate
user_id = sp.current_user()['id']


def create_playlist(user_id,term):
        playlist_name = 'My top songs ' + term
        playlist = sp.user_playlist_create(user= user_id, name= playlist_name,collaborative=False)
        return playlist['id']


#we only need to create the playlist once. 
repeat = os.path.isfile("playlist_ids.txt") 

if repeat == False:
    #creating the playlists for the first time 
    short_id = create_playlist(user_id,'from the last 4 weeks')
    medium_id = create_playlist(user_id,'from the last 6 months')
    long_id = create_playlist(user_id,'all time')

    print(short_id)
    #storing the playlist ids 
    playlist_ids = {'short_term':short_id,'medium_term':medium_id,'long_term':long_id}
    f = open("playlist_ids.txt", "w")
    f.write(str(playlist_ids))
    f.close()



#grabbing the playlist ids
f = open("playlist_ids.txt", "r")
content= f.read().replace("'", '"')
ids = json.loads(content)

#check if the playlist has been deleted ------------should this exist? on one hand, if accidently deleted, this is useful. On the other, this forces a playlist until script is stopped
still_here = sp.playlist_is_following(ids['short_term'],user_ids= [user_id])
x = still_here[0]
def update_playlist(user_id,period,playlist_id):
    results = sp.current_user_top_tracks(limit=50, offset=0, time_range=period)
    songs = pd.DataFrame(results['items'])
    tracklist = list(songs['id'])
    sp.user_playlist_replace_tracks(user_id, playlist_id, tracklist)
    return tracklist

if still_here[0] == True:
    update_playlist(user_id,'short_term',ids['short_term'])
    update_playlist(user_id,'medium_term',ids['medium_term'])
    update_playlist(user_id,'long_term',ids['long_term'])

elif still_here[0] == False:
    short_id = create_playlist(user_id,'from the last 4 weeks')
    medium_id = create_playlist(user_id,'from the last 6 months')
    long_id = create_playlist(user_id,'all time')

    #storing the playlist ids 
    playlist_ids = {'short_term':short_id,'medium_term':medium_id,'long_term':long_id}

    update_playlist(user_id,'short_term',short_id)
    update_playlist(user_id,'medium_term',medium_id)
    update_playlist(user_id,'long_term',long_id)


#####TO DO ----- if you delete the playlists, it will throw an error for update_playlist. Have an exception to check if the playlist exists (such function
##### exists in the spotipy) and if it does not, call the create playlist 

#make it run without pandas