import psycopg2
import json
import os

def fetch_albums(db_params):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    # Adjust the query if you have more fields (e.g., price, cover filename)
    cursor.execute("SELECT album_name, artist FROM album")
    albums = cursor.fetchall()
    conn.close()
    return albums

def build_album_data(albums, covers_dir="covers", price=99999):
    album_list = []
    for album_name, artist in albums:
        # Build the cover filename as in your download script
        cover_filename = f"{artist}_{album_name}.jpg".replace(" ", "_")
        # Remove invalid filename characters
        cover_filename = re.sub(r'[\\*?:"<>|]', "", cover_filename)
        cover_path = os.path.join(covers_dir, cover_filename)
        album_list.append({
            "title": album_name,
            "artist": artist,
            "cover": cover_path,
            "price": 99999  # You can fetch price from DB if you have it
        })
    return album_list

if __name__ == "__main__":
    import re
    db_params = {
        "dbname": "music_ranker",
        "user": "postgres",
        "password": "1234",
        "host": "localhost",
        "port": 5432
    }
    albums = fetch_albums(db_params)
    album_data = build_album_data(albums)
    with open("albums.json", "w", encoding="utf-8") as f:
        json.dump(album_data, f, ensure_ascii=False, indent=2)
    print("Exported album data to albums.json")