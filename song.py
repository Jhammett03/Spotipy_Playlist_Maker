import os
import spotipy
import spotipy.util as util
import random
import webbrowser

def create_playlist(song_name, artist_name, username):
    # Authenticate with Spotify
    scope = "playlist-modify-public"
    token = util.prompt_for_user_token(username, scope=scope)
    if not token:
        print("Authorization failed")
        return

    sp = spotipy.Spotify(auth=token)

    # Search for the song
    print("Searching for song:", song_name, "by", artist_name)
    query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=query, type="track")

    if not results['tracks']['items']:
        print("Song not found")
        return

    # Get track URI for the searched song
    searched_song_uri = results['tracks']['items'][0]['uri']

    # Find similar tracks
    similar_tracks = sp.recommendations(seed_tracks=[searched_song_uri], limit=100)

    if not similar_tracks['tracks']:
        print("No similar tracks found")
        return

    # Clear the list of track URIs
    track_uris = []

    # Get track URIs for the found tracks
    for track in similar_tracks['tracks']:
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
    song_name = input("Enter the song name: ")
    artist_name = input("Enter the artist name: ")
    username = "YOUR_USERNAME"  # Your Spotify username
    create_playlist(song_name, artist_name, username)

if __name__ == "__main__":
    main()
