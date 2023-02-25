# ClipStudioPaintDBExtractor
Extract SQLite3 DB file from a .clip Clip Studio Paint file

## About
This tool will let you choose a folder, from which it will recursively search for all .clip and .csp files, and extract the Sqlite3 Database from them to the same name.sqlite in the same folder.

You can then use a tool like [SQLiteStudio](https://sqlitestudio.pl/) To browse your file.

I probably haven't published a release, yet.

Sadly, the layer data isn't in the SQLite DB, but embedded as external data before it.  This can be extracted fairly easily, but nobody seems to have figured out what kind of compression is in use yet, so abandoning this project for now.


You can compile the binary like this:
```
pyinstaller --onefile --windowed csp_database_extractor.py 
```
