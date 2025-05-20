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
    # Ajusta los nombres de las columnas y la tabla según tu esquema real
    cursor.execute("""
        SELECT album, artist, track_number, song_name
        FROM song
        ORDER BY album, track_number
    """)
    songs = []
    for album, artist, track_number, song_name in cursor.fetchall():
        songs.append({
            "album_title": album,
            "artist": artist,
            "track_number": track_number,
            "track_title": song_name
        })
    conn.close()
    return songs

if __name__ == "__main__":
    songs = fetch_songs(db_params)
    with open("songs.json", "w", encoding="utf-8") as f:
        json.dump(songs, f, ensure_ascii=False, indent=2)
    print("songs.json exportado correctamente.")