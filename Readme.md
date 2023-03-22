# Convert your spotify "Favourites" into a Playlist

## Step-by-Step guid

### 0 - Setup env

Download this github repository on your machine and create a `virtual env`. No external libraries are needed for this
script.

### 1 - Get a Spotify access token

To run this script, you first need a Spotify access token, which you can get from any spotify developer console api
endpoint interface. Just open the `Spotify developer console` e.g.
`https://developer.spotify.com/console/get-current-user-playlists/` and click on the big green button labelled with
`GET TOKEN` and select the following scopes for the token:

-   user-library-read (get_tracks)
-   playlist-modify-public (create_playlist)
-   playlist-modify-private (create_playlist)
-   playlist-read-private (get_my_playlist)

**IMPORTANT**: If your token doesn't have exactly all the scopes specified above, the script will not work.

Add the new accesstoken to your `.env` file as:

```txt
SPOTIFY_ACCESS_TOKEN=<YOUR_ACCESS_TOKEN>
```

### Get your Spotify USER_ID

Open your spotify settings and go to your account overview to find your user id.

Otherwise you can request your user profile via the api which includes the user_id: `https://api.spotify.com/v1/me`

Add your USER_ID to your `.env` file as:

```txt
SPOTIFY_USER_ID=<YOUR_ACCESS_TOKEN>
```

### Configure the Script

Configure the script by setting the Playlist name in your .env file:

```conf
NAME_FAV_PLAYLIST='My Favourites - API'
```

### Run the main script

Run the main script with:

```sh
python main
```

Then, check that everything has worked by opening your spotify profile and opening the playlist you have created.
