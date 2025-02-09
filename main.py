import yt_dlp
import json
import threading
from pytubefix import YouTube
from moviepy import VideoFileClip
import os

total = 0
done = 0


def playlistToJson(playlist_url, output_file="playlist_videos.json"):
  ydl_opts = {
    'quiet': True,
    'extract_flat': True,
    'force_generic_extractor': True
  }
  
  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(playlist_url, download=False)
    
    if "entries" in info:
      video_urls = [entry["url"] for entry in info["entries"] if "url" in entry]

      with open(output_file, "w") as f:
        json.dump(video_urls, f, indent=2)
        
      print(f"Extracted {len(video_urls)} video URLs. Saved to {output_file}")
    else:
      print("No videos found in the playlist.")

def threadStarting(json_file):
  global total
  with open(json_file, "r") as f:
    video_urls = json.load(f)
  
  for url in video_urls:
    total+=1
    thread = threading.Thread(target=linkToAudioFile, args=(url,))
    thread.start()
    

def linkToAudioFile(link):
  global done,total
  yt = YouTube(link)
  stream = yt.streams.get_audio_only(subtype='mp4')
  path = stream.download(output_path='./songs', max_retries=10)
  done+=1
  print(str(done)+"/"+str(total))
  mp4Tomp3(path=path)

def mp4Tomp3(path):
  base, ext = os.path.splitext(path)
  new_file = base + '.mp3'
  os.rename(path, new_file)

playlist_url = "https://www.youtube.com/playlist?list=PLFL5k0qCklRoTvtOcAX5OAuokjcT2mV-H"
playlistToJson(playlist_url)
threadStarting("playlist_videos.json")



