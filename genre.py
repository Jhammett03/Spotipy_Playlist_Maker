import os
import spotipy
import spotipy.util as util
import random
import webbrowser

def authenticate(username):
    # Authenticate with Spotify
    scope = "playlist-modify-public"
    token = util.prompt_for_user_token(username, scope=scope)
    if not token:
        print("Authorization failed")
        return None
    return token

def create_playlist(genre, username):
    token = authenticate(username)
    if not token:
        return

    sp = spotipy.Spotify(auth=token)

    # Search for tracks in the specified genre
    print("Searching for tracks in the genre:", genre)
    total_tracks = 200  # Desired total number of tracks
    tracks_per_request = 50  # Maximum number of tracks per request
    num_requests = (total_tracks + tracks_per_request - 1) // tracks_per_request

    track_uris = []

    for _ in range(num_requests):
        results = sp.search(q=f"genre:{genre}", type="track", limit=tracks_per_request)

        if not results['tracks']['items']:
            print("No tracks found for the specified genre")
            return

        # Get track URIs for the found tracks
        for track in results['tracks']['items']:
            track_uris.append(track['uri'])

    # Shuffle the list of track URIs
    random.shuffle(track_uris)

    # Prompt for playlist name
    playlist_name = input('Playlist Name: ')

    # Create a new playlist
    playlist = sp.user_playlist_create(username, playlist_name, public=True)

    # Add tracks to the playlist in batches
    batch_size = 100
    for i in range(0, len(track_uris), batch_size):
        batch_tracks = track_uris[i:i + batch_size]
        sp.playlist_add_items(playlist['id'], batch_tracks)

    print(f"Playlist '{playlist_name}' created successfully")

    # Open the playlist in a web browser
    playlist_url = playlist['external_urls']['spotify']
    webbrowser.open(playlist_url)


def main():
    genre = input("Enter the genre: ")
    username = "YOUR_USERNAME"  # Replace with your Spotify username
    create_playlist(genre, username)

if __name__ == "__main__":
    main()
