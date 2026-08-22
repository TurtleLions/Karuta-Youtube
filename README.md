# Getting Started

Create venv with
```bash
python3 -m venv /path/to/venv
```

Activate venv with
```bash
source /path/to/venv
```

Install libraries with
```bash
pip install -r requirements.txt
```

To run webpage
```bash
python3 server.py
```

Open link shown in terminal

# Note about yt-dlp

If yt-dlp is bugging you about a JS runtime when you try downloading, try following the steps here: `https://github.com/yt-dlp/yt-dlp/wiki/EJS`. 

If you are receiving 403 forbidden errors from yt-dlp, it is possible either yt-dlp is not updated (try `pip install -U "yt-dlp[default,curl-cffi]"`) or YouTube has potentially broken yt-dlp temporarily. If that is not enough as well, you can try using a nightly build as well, using `pip install -U --pre "yt-dlp[default,curl-cffi]"`, although this is not a stable solution. 

# Note About Song Storage and Downloading

Unfortunately, I've changed the expectation for how songs are stored *again* in this version. If you are using this version for actual song playing purposes, this version expects two folders:

- A `playlists` directory. It should contain various `.json` files, each containing the names of the songs within its deck. So you may have a file called `ani1.json` in this directory, and in the file it should have a list of the names of all the songs in the ani1 deck.
- A `stored-songs` directory. This directory contains sub directories, with each sub directory being a deck. There must be a match between the names in `playlists` and `stored-songs`. So if you have a deck called `my_deck_123.json` in the `playlists` folder, there should be a folder called `my_deck_123` in `stored-songs`. The text contents of `my_deck_123.json` and the audio file contents of `my_deck_123` should match up name-wise as well. 

The main reason for this was to allow you to select and change decks without the need to go into your file system.

That being said, the song downloader for this version should handle this for you automatically, both creating the files in `playlists` and the subdirectories within `stored-songs` with the right formatting and naming and whatnot. In the foreseeable future, I will do my best to keep this branch's downloader updated and functional.

Do remember, if you manually change either the `.json` file's or `stored-songs` sub-directory's name, you should change the other's! 

That all being said, it is possible you get a folder of audio files from somewhere else like Google Drive, or are simply just using this branch for the purposes of downloading a deck and using your normal Karuta player. In that case:

## Given a folder of audio files, you need to get them playing on this version

1. Make sure to put the folder into the `stored-songs` folder. It should look like
```
+ stored-songs
|---+ my_deck
    |---- song1.mp3
    |---- song2.mp3
    |---- song3.mp3
    |---- song4.mp3
    ... and such forth
|---+ some_other_deck
```

2. I've provided a Python script to create the `playlists` file for you. Assuming the folder you uploaded is called `my_deck`, run in your terminal:

```bash
python3 fixme.py "my_deck"
```

It should print the number of songs within your folder. You can check the `playlists` folder if the `.json` file has been created, and if it's there and looks right, that's all.

## You just need the audio files from the downloader, and want to move them to another downloader

It depends which version of the Karuta player you have.

On the "classic" Karuta players, like the `best-version` branch (as of August 2026), you only need the folder of audio files, which you can locate in the `stored-songs` directory.

On other versions, like the `main` branch (as of August 2026), you need both the folder of audio files, which you can locate in the `stored-songs` directory, as well as the same `.json` file from the `playlists` directory to put into your other `playlists` directory.

Note that if you do not provide a name for the deck that you just downloaded, it will use a timestamp instead.

# Images (and names) for Online Karuta

As you may know, there is currently a version of Karuta Online in the works. If you would like to provide a deck, this branch creates the least headache for me specifically if you want custom song names and images on the cards.

1. Either have or download the deck you want to edit. At the bare minimum, you need the `.json` file, so you can use the `fixme.py` python script above if you only have the song files.

It's important to note that on my end, if there's a mismatch on the names of the songs (e.g. an audio file with the root name `Literature` and an image file with the root name `Literature (Reina Ueda)`), I'll need to go back and look over all the differences to fix them. Put simply, whatever song names you currently have for your audio files and inside your `playlist/deck_name.json` file should match whatever I'm able to get. If you never changed the actual file names of the audio files from where you originally got them (whether it be one of the Karuta song downloaders or a Google Drive), then I can get the same file names and we're most likely all good. Alternatively, if you *did* change them, you can also send me your edited audio files later, and I can work off of that.

2. Open the local website, and go to the "Edit" tab at the top right, then select the deck you're interested in from the drop down menu.

3. This should open up a table with 3 columns. 

- The left column will be filled with file names. 
- The middle column has text boxes in each row, and if you'd like to add a custom name to a particular song (for example, an English translation of a title or adding the artist's name), you can enter it here.
- The right column can contain images. To upload an image, copy it from somewhere, click on the cell you'd like to add the image to, and paste. Note that copying an image from something like Google Slides or Canva will unfortunately not work, but copying an image from Google Search, most websites, or even Discord should work. You can delete the image by clicking the cell and hitting the backspace key.

4. Once you're done making the edits you want, save your changes. There are two buttons near the top of the page. One of them will save the custom names that you added (the middle column), and the other will save the custom images that you added (the right column). 

With respect to the custom names, this will create a new file to define the custom names, rather than actually modifying the audio file names.

5. You can now send me the files for me to upload to the online version.

- If you made text changes (middle column), then within the `custom` folder on your repo, there should be a `.json` file that lists all of the custom names you added, which you can send me.
- If you made image changes (right column), then within the `images` folder on your repo, there should be a subfolder (with the same `.json` name) that contains all the custom images you uploaded, which you can send to me.