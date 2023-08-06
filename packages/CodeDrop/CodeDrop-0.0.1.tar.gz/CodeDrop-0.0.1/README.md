This script uses Dropbox API to upload your python code to your Dropbox app folder.

How to use:

1. Create a new app from the dropbox developer section and get the access token,
2. Insert your dropbox access token between "" on line 16 of codedrop.py,
3. Import codedrop in your python script and use drop() function to upload codes to your dropbox app folder.

drop() needs two parameters, file_source & file_name. Type __file__ for file_source and your desired string for file_name.

Example:

drop(__file__, "test-drop")