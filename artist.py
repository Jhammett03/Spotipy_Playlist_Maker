import os
import spotipy
import spotipy.util as util
import random
import webbrowser

def create_playlist(artist_name, username):
    # Authenticate with Spotify
    scope = "playlist-modify-public"
    token = util.prompt_for_user_token(username, scope=scope)
    if not token:
        print("Authorization failed")
        return

    sp = spotipy.Spotify(auth=token)

    # Search for the artist
    print("Searching for artist:", artist_name)
    results = sp.search(q=artist_name, type="artist")

    if not results['artists']['items']:
        print("Artist not found")
        return
   

    artist_id = results['artists']['items'][0]['id']

    # Clear the list of track URIs
    top_tracks_uris = []

    # Get top tracks for the artist
    tracks = sp.artist_top_tracks(artist_id)
    top_tracks_uris.extend([track['uri'] for track in tracks['tracks']])

    # Get related artists
    related_artists = sp.artist_related_artists(artist_id)
    for artist in related_artists['artists']:
        tracks = sp.artist_top_tracks(artist['id'])
        top_tracks_uris.extend([track['uri'] for track in tracks['tracks']])

    # Shuffle the list of track URIs
    random.shuffle(top_tracks_uris)

    # Prompt for playlist name
    playlist_name = input('Playlist Name: ')

    # Create a new playlist
    playlist = sp.user_playlist_create(username, playlist_name, public=True)

    # Add tracks to the playlist in batches
    batch_size = 100
    for i in range(0, len(top_tracks_uris), batch_size):
        batch_tracks = top_tracks_uris[i:i + batch_size]
        sp.playlist_add_items(playlist['id'], batch_tracks)
    
    print(f"Playlist '{playlist_name}' created successfully")

    # Open the playlist in a web browser
    playlist_url = playlist['external_urls']['spotify']
    webbrowser.open(playlist_url)

def main():
    artist_name = input("Enter the artist name: ")
    #username = input("Enter your Spotify username: ")
    username = "YOUR_USERNAME"
    create_playlist(artist_name, username)

if __name__ == "__main__":
    main()
