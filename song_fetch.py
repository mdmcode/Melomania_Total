import psycopg2
import json

# Ajusta estos parámetros según tu base de datos
db_params = {
    "dbname": "music_ranker",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": 5432
}

def fetch_songs(db_params):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    # Updated query with JOIN to get artist name instead of artist_id
    cursor.execute("""
        SELECT album.album_name, artist.artist_name, song.track_number, song.song_name
        FROM song
        JOIN album ON song.album = album.album_name
        JOIN artist ON album.artist_id = artist.id
        ORDER BY album.album_name, song.track_number
    """)
    songs = []
    for album_title, artist_name, track_number, song_name in cursor.fetchall():
        # Clean the data
        album_title = album_title.strip() if isinstance(album_title, str) else album_title
        artist_name = artist_name.strip() if isinstance(artist_name, str) else artist_name
        song_name = song_name.strip() if isinstance(song_name, str) else song_name
        
        songs.append({
            "album_title": album_title,
            "artist": artist_name,
            "track_number": track_number,
            "track_title": song_name
        })
    conn.close()
    return songs

if __name__ == "__main__":
    songs = fetch_songs(db_params)
    with open("songs.json", "w", encoding="utf-8") as f:
        json.dump(songs, f, ensure_ascii=False, indent=2)
    print(f"songs.json exportado correctamente con {len(songs)} canciones.")