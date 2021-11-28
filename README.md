# placetel-recording-downloader
Download and delete Call recordings from Placetel via the web API

# Setup

```bash
pip3 install -r requirements.txt
```

You need to rename `setting.ini.example` to `settings.ini`.

Then you need to edit all the settings within `settings.ini`.

# Running

This project is tested for python 3.9

```
python3 main.py
```

# Caveats

This project does not:

- consider API limits
- validate downloaded files
- order the files into folders
- download recordings from the current day

# TODO

- write list of downloaded and deleted files
- add option to order files into iso8601 ordered folders (./YYYY/MM/DD/\*.mp3)
