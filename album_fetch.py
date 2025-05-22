import psycopg2
import requests
import os
import re
import urllib.parse

# Evita que el nombre del archivo tenga caracteres invalidos
def sanitize_filename(filename):
    filename = re.sub(r'[\\*?:"<>|\r\n]', "", filename)
    filename = filename.strip() 
    return filename

# Se conecta a la base de datos y selecciona el nombre y el artista de los albums en la tabla album
def fetch_albums(db_params):
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT album.album_name, artist.artist_name 
            FROM album 
            JOIN artist ON album.artist_id = artist.id
        """)
        albums = cursor.fetchall()
        conn.close()
        return albums
    
def get_spotify_token(client_id, client_secret):
    import requests
    import base64
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': 'client_credentials'}
    response = requests.post(auth_url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()['access_token']

def download_cover_itunes(title, artist, save_dir="covers"):
    import requests, os, re, urllib.parse
    os.makedirs(save_dir, exist_ok=True)
    query = f"{artist} {title}"
    url = f"https://itunes.apple.com/search?term={urllib.parse.quote(query)}&entity=album&limit=1"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"iTunes fetch failed for {artist}_{title}")
        return False
    try:
        data = response.json()
    except Exception as e:
        print(f"Error decoding JSON for {artist} - {title}: {e}")
        print("Response content:", response.text)
        return False
    if data.get('resultCount', 0) > 0:
        cover_url = data['results'][0]['artworkUrl100']
        img_data = requests.get(cover_url).content
        raw_filename = f"{save_dir}/{artist}_{title}_itunes.jpg".replace(" ", "_")
        filename = sanitize_filename(raw_filename)
        with open(filename, "wb") as f:
            f.write(img_data)
        print(f"Downloaded from iTunes: {filename}")
        return True
    else:
        print(f"No cover found on iTunes for {artist} - {title}")
        return False
    
def download_cover_lastfm(title, artist, api_key='1373dea53f05ccbb3143a0660d0be3ab', save_dir="covers"):
    import requests, os, urllib.parse
    os.makedirs(save_dir, exist_ok=True)
    url = f"http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={api_key}&artist={urllib.parse.quote(artist)}&album={urllib.parse.quote(title)}&format=json"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Last.fm fetch failed for {artist}_{title}")
        return False
    data = response.json()
    if 'album' in data and 'image' in data['album']:
        # Get the largest image (usually 'extralarge')
        images = data['album']['image']
        large_image = next((img['#text'] for img in images if img['size'] == 'extralarge'), None)
        if large_image:
            img_data = requests.get(large_image).content
            raw_filename = f"{save_dir}/{artist}_{title}_lastfm.jpg".replace(" ", "_")
            filename = sanitize_filename(raw_filename)
            with open(filename, "wb") as f:
                f.write(img_data)
            print(f"Downloaded from Last.fm: {filename}")
            return True
    print(f"No cover found on Last.fm for {artist} - {title}")
    return False

def download_cover(title, artist, token, save_dir="covers"):
    import requests, os, urllib.parse
    os.makedirs(save_dir, exist_ok=True)
    query = f"album:{title} artist:{artist}"
    url = f"https://api.spotify.com/v1/search?q={urllib.parse.quote(query)}&type=album&limit=1"
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Spotify fetch failed for {artist}_{title}")
        return False
    data = response.json()
    items = data.get('albums', {}).get('items', [])
    if items:
        cover_url = items[0]['images'][0]['url']
        img_data = requests.get(cover_url).content
        raw_filename = f"{save_dir}/{artist}_{title}.jpg".replace(" ", "_")
        filename = sanitize_filename(raw_filename)
        with open(filename, "wb") as f:
            f.write(img_data)
        print(f"Downloaded from Spotify: {filename}")
        return True
    else:
        print(f"No cover found on Spotify for {artist} - {title}")
        return False

if __name__ == "__main__":
    client_id = "40fd9553347041b1a8239f87afd5c979"
    client_secret = "270b68f63e3c49409c34f95977d17b07"
    spotify_token = get_spotify_token(client_id, client_secret)
    db_params = {
        "dbname": "music_ranker",
        "user": "postgres",
        "password": "1234",
        "host": "localhost",
        "port": 5432
    }
    albums = fetch_albums(db_params)
    print(f"Found {len(albums)} albums in database")
    
    downloaded_count = 0
    processed_count = 0
    
    for name, artist in albums:
        processed_count += 1
        name = name.strip() if isinstance(name, str) else name
        artist = artist.strip() if isinstance(artist, str) else artist
        print(f"Processing {processed_count}/{len(albums)}: '{name}' by '{artist}'")
        
        found = download_cover(name, artist, spotify_token)
        if found:
            downloaded_count += 1
        else:
            lastfm_found = download_cover_lastfm(name, artist)
            if lastfm_found:
                downloaded_count += 1
            else:
                itunes_found = download_cover_itunes(name, artist)
                if itunes_found:
                    downloaded_count += 1
    
    print(f"\nSummary: Processed {processed_count} albums, downloaded {downloaded_count} covers")