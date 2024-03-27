import os
import spotipy
import spotipy.util as util
import random
import webbrowser

def create_playlist_from_artist(artist_name, username):
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

def create_playlist_from_song(song_name, artist_name, username):
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

def create_playlist_from_genre(genre, username):
    scope = "playlist-modify-public"
    token = util.prompt_for_user_token(username, scope=scope)
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

def create_playlist_from_album(album_name, artist_name, username):
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
    print("Options:\n1. Create playlist from artist\n2. Create playlist from song\n3. Create playlist from genre\n4. Create playlist from album\n5. Exit\n")
    option = input("Option: ")
    print()
    username = "YOUR_USERNAME"
    if option == "1":
        artist_name = input("Enter the artist name: ")
        create_playlist_from_artist(artist_name, username)
    elif option == "2":
        song_name = input("Enter the song name: ")
        artist_name = input("Enter the artist name: ")
        create_playlist_from_song(song_name, artist_name, username)
    elif option == "3":
        genre = input("Enter the genre: ")
        create_playlist_from_genre(genre, username)
    elif option == "4":
        album = input("Enter the album name: ")
        artist = input("Enter the artist name: ")
        create_playlist_from_album(album, artist, username)
    elif option == "5":
        print("Exiting...")
    else:
        print("Invalid option")

if __name__ == "__main__":
    main()
