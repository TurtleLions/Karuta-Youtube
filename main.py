import yt_dlp
import json
import threading
from pytubefix import YouTube
import os
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.services.storage import Storage
import keys

client = Client()
client.set_endpoint("https://cloud.appwrite.io/v1")
client.set_project(keys.project_id)
client.set_key(keys.api_key)

database = Databases(client)
storage = Storage(client)

SONGS_COLLECTION_ID = keys.songs_id
PROGRESS_COLLECTION_ID = keys.progress_id
BUCKET_ID = keys.bucket_id

total = 0
done = 0


def update_progress():
    """Update download progress in Appwrite Database"""
    database.update_document(
        "karuta_db",
        PROGRESS_COLLECTION_ID,
        "progress_doc",
        {"done": done, "total": total}
    )


def playlistToJson(playlist_url, output_file="playlist_videos.json"):
    """Extract video URLs from a YouTube playlist"""
    ydl_opts = {'quiet': True, 'extract_flat': True, 'force_generic_extractor': True}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)
        if "entries" in info:
            video_urls = [entry["url"] for entry in info["entries"] if "url" in entry]

            with open(output_file, "w") as f:
                json.dump(video_urls, f, indent=2)

            print(f"Extracted {len(video_urls)} video URLs. Saved to {output_file}")
        else:
            print("No videos found in the playlist.")


def upload_song(file_path):
    """Upload MP3 file to Appwrite Storage"""
    with open(file_path, "rb") as f:
        response = storage.create_file(BUCKET_ID, "unique()", f)

    return response["$id"]


def linkToAudioFile(link):
    """Download & convert video to MP3, then upload to Appwrite"""
    global done
    yt = YouTube(link)
    stream = yt.streams.get_audio_only(subtype='mp4')
    path = stream.download(output_path='./songs', max_retries=10)

    done += 1
    update_progress()

    mp3_path = mp4Tomp3(path)
    file_id = upload_song(mp3_path)

    database.create_document(
        "karuta_db",
        SONGS_COLLECTION_ID,
        "unique()",
        {"name": os.path.basename(mp3_path), "url": file_id, "played": False}
    )


def mp4Tomp3(path):
    """Convert MP4 audio file to MP3"""
    base, ext = os.path.splitext(path)
    new_file = base + '.mp3'
    os.rename(path, new_file)
    return new_file


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("No playlist URL provided.")
        sys.exit(1)

    playlist_url = sys.argv[1]
    playlistToJson(playlist_url)

    with open("playlist_videos.json", "r") as f:
        video_urls = json.load(f)

    total = len(video_urls)
    update_progress()

    for url in video_urls:
        thread = threading.Thread(target=linkToAudioFile, args=(url,))
        thread.start()
