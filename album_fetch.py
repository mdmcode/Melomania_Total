import psycopg2
import requests
import os
import re
import urllib.parse

def sanitize_filename(filename):
    return re.sub(r'[\\*?:"<>|]', "", filename)

def fetch_albums(db_params):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    cursor.execute("SELECT album_name, artist FROM album")
    albums = cursor.fetchall()
    conn.close()
    return albums

def download_cover(title, artist, save_dir="covers"):
    os.makedirs(save_dir, exist_ok=True)
    query = f"{artist} {title}"
    url = f"https://itunes.apple.com/search?term={query}&entity=album&limit=1"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Fetch fallado para {artist}_{title}")
        return
    try:
        data = response.json() 
    except Exception as e:
        print(f"Error decoding JSON for {artist} - {title}: {e}")
        print("Response content:", response.text)
        return
    if data['resultCount'] > 0:
        cover_url = data['results'][0]['artworkUrl100']
        img_data = requests.get(cover_url).content
        raw_filename = f"{save_dir}/{artist}_{title}.jpg".replace(" ", "_")
        filename = sanitize_filename(raw_filename)
        with open(filename, "wb") as f:
            f.write(img_data)
        print(f"Downloaded: {filename}")
    else:
        print(f"No cover found for {artist} - {title}")

if __name__ == "__main__":
    db_params = {
        "dbname": "music_ranker",
        "user": "postgres",
        "password": "1234",
        "host": "localhost",
        "port": 5432
    }
    albums = fetch_albums(db_params)
    for name, artist in albums:
        download_cover(name, artist)