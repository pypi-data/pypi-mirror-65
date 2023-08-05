# YouTube Utilities
##Load Comments
Comments loader.   Converts a batch of comments files in JSON format into a SQLite 3database.
Tested on Windows 10, but there isn't any Windows's specific code in the application.
###new comments.db
Shell SQLite database used by Load Comments
##Load Subtitles
Loads metadata for JSON files created by downloading video metadata with youtube-dl.
Mostly used to load subtitle data, but could be extended to load any metadata.
##FetchSubtitles.py
Library called by other routines.
##magnum chorum.txt
Sample batch file used by youtube-dl to download subtitles
##YouTube to JSON.py
Library used by the loader programs.
 