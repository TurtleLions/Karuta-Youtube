import os
import json
import unicodedata
import sys

if len(sys.argv) < 2:
    print("provide a deck name, e.g. `python3 fixme.pe by2011_karuta")
    sys.exit(1)

DECK_NAME = sys.argv[1]

song_dir = f"stored-songs/{DECK_NAME}"
misc_path = f"ppap/{DECK_NAME}.json"

filenames = [f for f in os.listdir(song_dir)]
filenames = [unicodedata.normalize('NFC', f) for f in filenames]

print(len(filenames))

if not os.path.exists("playlists"):
    os.makedirs("playlists")

with open(misc_path, 'w') as f:
    json.dump(filenames, f, indent=4, sort_keys=True)


