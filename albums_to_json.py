import psycopg2
import json
import os

# Ajusta estos parámetros según tu base de datos
db_params = {
    "dbname": "music_ranker",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": 5432
}

def fetch_albums_for_json(db_params):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT album.album_name, artist.artist_name, album.release_year
        FROM album 
        JOIN artist ON album.artist_id = artist.id
        ORDER BY album.album_name
    """)
    albums = []
    for album_name, artist_name, release_year in cursor.fetchall():
        # Clean the names
        album_name = album_name.strip() if isinstance(album_name, str) else album_name
        artist_name = artist_name.strip() if isinstance(artist_name, str) else artist_name
        
        # Generate cover path (assuming your covers follow this pattern)
        cover_filename = f"{artist_name}_{album_name}.jpg".replace(" ", "_")
        # Sanitize filename
        import re
        cover_filename = re.sub(r'[\\*?:"<>|\r\n]', "", cover_filename)
        cover_path = f"covers\\{cover_filename}"
        
        # Check if cover file actually exists
        if not os.path.exists(cover_path):
            # Try alternative naming patterns
            alt_patterns = [
                f"covers\\{artist_name}_{album_name}_spotify.jpg".replace(" ", "_"),
                f"covers\\{artist_name}_{album_name}_lastfm.jpg".replace(" ", "_"),
                f"covers\\{artist_name}_{album_name}_itunes.jpg".replace(" ", "_")
            ]
            for pattern in alt_patterns:
                pattern = re.sub(r'[\\*?:"<>|\r\n]', "", pattern)
                if os.path.exists(pattern):
                    cover_path = pattern
                    break
            else:
                print(f"Warning: No cover found for {artist_name} - {album_name}")
                cover_path = "covers\\default_cover.jpg"  # fallback
        
        albums.append({
            "title": album_name,
            "artist": artist_name,
            "cover": cover_path,
            "price": 99999  # Default price, adjust as needed
        })
    
    conn.close()
    return albums

if __name__ == "__main__":
    albums = fetch_albums_for_json(db_params)
    with open("albums.json", "w", encoding="utf-8") as f:
        json.dump(albums, f, ensure_ascii=False, indent=2)
    print(f"albums.json exportado correctamente con {len(albums)} álbumes.")