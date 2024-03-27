import spotipy
import spotipy.util as util
import random
import webbrowser

def create_playlist(album_name, artist_name, username):
    # Authenticate with Spotify
    scope = "playlist-modify-public"
    token = util.prompt_for_user_token(username, scope=scope)
    if not token:
        print("Authorization failed")
        return

    sp = spotipy.Spotify(auth=token)

    # Search for the specified album
    print("Searching for album:", album_name, "by", artist_name)
    query = f"album:{album_name} artist:{artist_name}"
    album_results = sp.search(q=query, type="album")

    if not album_results['albums']['items']:
        print("Album not found")
        return

    # Get the specified album ID
    album_id = album_results['albums']['items'][0]['id']

    # Get tracks from the specified album
    album_tracks = sp.album_tracks(album_id)

    if not album_tracks['items']:
        print("No tracks found in the album")
        return

    # Extract track URIs from the specified album tracks
    track_uris = [track['uri'] for track in album_tracks['items']]

    # Find related albums based on the artist of the specified album
    artist_id = album_results['albums']['items'][0]['artists'][0]['id']
    related_albums = sp.artist_albums(artist_id)

    # Extract track URIs from tracks of related albums
    for related_album in related_albums['items']:
        # Avoid fetching tracks from the specified album again
        if related_album['id'] != album_id:
            related_album_tracks = sp.album_tracks(related_album['id'])
            track_uris.extend([track['uri'] for track in related_album_tracks['items']])

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
    album_name = input("Enter the album name: ")
    artist_name = input("Enter the artist name: ")
    username = "YOUR_USERNAME"  # Your Spotify username
    create_playlist(album_name, artist_name, username)

if __name__ == "__main__":
    main()
