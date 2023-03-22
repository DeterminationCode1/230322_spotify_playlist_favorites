import json
import requests
import datetime
import os

# Constants for Development
URL_PREFIX = "https://api.spotify.com/v1/"
# Nr. of songs loaded by each request. Max 20.
FAV_LIMIT = 20
get_favorites_ulr = f"me/tracks?limit={FAV_LIMIT}"

OATUH_TOKEN = os.environ.get('SPOTIFY_ACCESS_TOKEN')
headers = {"Authorization": f"Bearer {OATUH_TOKEN}"}

# Get the spotify user_id by requesting your profile with:	`https://api.spotify.com/v1/me` > id
USER_ID = os.environ.get('SPOTIFY_USER_ID')

URL_FAVORITES_ROOT = URL_PREFIX + get_favorites_ulr

def get_tracks(url: str):
    '''
    Required scopes for this endpoint:
    - user-library-read
    
    https://developer.spotify.com/console/get-current-user-saved-tracks/
    '''
    
    result = requests.get(url, headers=headers).content
    result = json.loads(result)
        # external_urls: the link of the track on spotify
    # external_ids
    tracks = [t['track']  for t in result['items']]
    # urls to all songs in your favorite list
    track_urls = [t['uri'] for t in tracks]
    next = result['next']
    return [track_urls, next]

def get_all_tracks(url):
    itteration = 1
    all_results = []
    while url:
        [res, next] = get_tracks(url)
        all_results += res
        url = next
        print(f"{itteration * FAV_LIMIT} songs loaded")
        itteration += 1
    print(f"SUCCESS: All {itteration * FAV_LIMIT} songs have been loaded.")
    return all_results

def create_new_playlist(name):
    '''
    Required scopes for this endpoint:

    - playlist-modify-public
    - playlist-modify-private

    get user id: https://github.com/spotipy-dev/spotipy/issues/336

    ---
    official [docs](https://developer.spotify.com/console/post-playlists/?user_id=&body=%7B%22name%22%3A%22New%20Playlist%22%2C%22description%22%3A%22New%20playlist%20description%22%2C%22public%22%3Afalse%7D)
    '''
    URL = f'https://api.spotify.com/v1/users/{USER_ID}/playlists'
    data = {
        "name": name,
        "description": "New playlist description",
        "public": False
        }
    res = requests.post(URL,data=json.dumps(data), headers=headers)
    print(res)
    return res

def check_access_token_expired():
    '''Check that your spotify access token is not expired.

    For this check, a simple request to get your playlists is made, which should alaways work.
    '''
    URL = 	'me/playlists'
    res = requests.get(f"{URL_PREFIX}{URL}",headers=headers).content
    res = json.loads(res)
    print(res, 'grrr')
    error = res.get('error')
    print(error, 'ggtr')
    if error:
        print('hif')
        msg = error.get('message')
        status = error.get('status')
        print(msg,status, '1qed')
        if msg == 'The access token expired' and status == 401:
            return True
    return False 

def get_my_playlists():
    '''Get the playlists of the oauth token user.

    BE AWARE: if your token does not have the private scope, only public playlists will be returned.

    Requires:
    - playlist-read-private
    '''
    URL = 	'me/playlists'
    res = requests.get(f"{URL_PREFIX}{URL}",headers=headers).content
    res = json.loads(res)
    return res['items']

def get_playlist_nr_tracks(name):
    '''Get the total number of tracks in a playlist. 
    
    E.g. if the playlist "My Favorites - API" has 102 songs, it will return: `102`.
    '''
    playlists = get_my_playlists()
    count = None
    for p in playlists:
        print(p['name'], 'dfdfd')
        if p['name'] == name:
            print(p, 'rgr')
            count = p['tracks']['total']
            break
    if not count:
        raise ValueError("Playlist could not be found.")
    return count

def get_id_of_playlist_by_name(name):
    playlists = get_my_playlists()
    id = None
    for p in playlists:
        print(p['name'], 'dfdfd')
        if p['name'] == name:
            id = p['id']
            break
    if not id:
        raise ValueError("Playlist could not be found.")
    return id


def add_songs_to_playlist(playlist_id, songs):
    '''
    A maximum of 100 items can be added in one request. 
    '''
    URL = f'playlists/{playlist_id}/tracks'
    total_nr_songs = len(songs)
    print(type(songs))
    print(songs)

    while songs:
        data = {"uris": songs[:100]}
        res = requests.post(f"{URL_PREFIX}{URL}", data=json.dumps(data), headers=headers)
        print(res)
        # delete first 100 songs
        songs = songs[100:]
    print(f"Success, added songs to playlist {playlist_id}")

def remove_songs_from_playlist(playlist_id, songs):
    '''
    A maximum of 100 items can be added in one request. 
    '''
    URL = f'playlists/{playlist_id}/tracks'
    total_nr_songs = len(songs)
    print(type(songs))
    print(songs)

    while songs:
        data = {"uris": songs[:100]}
        print(type(data), 'feew', data,)
        res = requests.delete(f"{URL_PREFIX}{URL}", data=json.dumps(data), headers=headers)
        # delete first 100 songs
        songs = songs[100:]
    print(f"Success, removed songs from playlist {playlist_id}")

# Configure the end result
# The new playlist containing all your favourites will be called:
NAME_FAV_PLAYLIST = os.environ.get('NAME_FAV_PLAYLIST') # f'My Favourites - { datetime.datetime.today().date()}'
# You cannot delete a playlist


def main():
    # Check access token form spotify is valid:
    print(check_access_token_expired(), 'grr')
    if check_access_token_expired():
        raise ValueError("""\
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!! ERROR !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Your Spotify \"Access Token\" has expired.
To fix this error, please go to the spotify developer console and request a new one. For example, at https://developer.spotify.com/console/get-current-user-playlists/ > GET TOKEN (button)

Make sure to give it all the required scopes:
- user-library-read   (get_tracks)
- playlist-modify-public  (create_playlist)
- playlist-modify-private  (create_playlist)
- playlist-read-private  (get_my_playlist)

!!!!!!!!!!!!!!!!!!!!!!!!!! ERROR !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\
""")
    try:
        fav_playlist_id = get_id_of_playlist_by_name(NAME_FAV_PLAYLIST)
    except ValueError as e:
        # If playlist name doesn't exist. Create a new playlist with the name.
        res_create_play = create_new_playlist(NAME_FAV_PLAYLIST)
        assert res_create_play.status_code == 201

    fav_tracks = get_all_tracks(url=URL_FAVORITES_ROOT)
    # For Debugging, you can use the following to only request 20 items instead of all:
    # [fav_tracks, next] = get_tracks(url=URL_FAVORITES_ROOT) 

    remove_songs_from_playlist(fav_playlist_id, fav_tracks)

    add_songs_to_playlist(fav_playlist_id, fav_tracks)

    # ================= Assert Test everything worked. ====================
    count_tracks_new = get_playlist_nr_tracks(NAME_FAV_PLAYLIST)
    assert count_tracks_new == len(fav_tracks)

    print("\n=============================================================================")
    print(f"==== Successfully, updated playlist \"{NAME_FAV_PLAYLIST}\" with {count_tracks_new} songs. =====")
    print("=============================================================================")

if __name__ == '__main__':
    main()
