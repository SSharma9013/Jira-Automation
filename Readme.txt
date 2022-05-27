It is a python script which creates all six jiras that is supposed to be created whenever there is a new version of Skype released.Will have to run is manually when we need to create the tickets.
Python 3 or more required.

Fill in the details in the config.ini
email = YOUR_EMAIL
AccessToken = YOUR_ACCESS_TOKEN 
SkypeVersion = LATEST_VERSION_FOR_WHICH_TICKET_NEED_TO_BE_CREATED
FixVersion = IMPM_LATEST_RELEASED_VERSION

After making the config changes Run the python script in command prompt
python main.py


