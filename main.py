import yt_dlp
from youtubesearchpython import VideosSearch

def search_and_download(song_name):
    # Search for the song on YouTube
    search = VideosSearch(song_name, limit=10)  # Increase limit to get more results to filter
    result = search.result()
    
    if not result['result']:
        print(f"No results found for: {song_name}")
        return
    
    # Maximum duration in seconds (10 minutes)
    max_duration = 10 * 60
    
    # Find the first video that meets the duration criteria out of the top 10 results
    video_url = None
    for video in result['result']:
        duration_str = video['duration']
        if duration_str:
            parts = duration_str.split(':')
            if len(parts) == 2:
                minutes, seconds = map(int, parts)
                duration = minutes * 60 + seconds
            elif len(parts) == 3:
                hours, minutes, seconds = map(int, parts)
                duration = hours * 3600 + minutes * 60 + seconds
            else:
                continue
            
            if duration <= max_duration:
                video_url = video['link']
                break
    
    if video_url is None:
        print(f"No video found with duration less than or equal to 10 minutes for: {song_name}")
        return
    
    print(f"Downloading: {song_name} from {video_url}")

    # Download options
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{song_name}.%(ext)s', # U can specify the download path(it should be absolute path)
        'quiet': True,
        'ffmpeg_location': 'C:/ffmpeg/bin'  # Specify the path to ffmpeg
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    print(f"Downloaded: {song_name}.mp3")

def load_songs_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            songs = [line.strip() for line in file.readlines()]
        return songs
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []

if __name__ == "__main__":
    # File path to the text file containing the list of song names
    file_path = 'songs.txt'
    
    # Load songs from the text file
    songs = load_songs_from_file(file_path)
    
    # Download each song
    for song in songs:
        if song:  # Check if the line is not empty
            search_and_download(song)