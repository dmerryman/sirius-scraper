from pysosirius import PySoSirius
import time
import datetime
from twython import Twython
from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

sirius = PySoSirius()
twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)
channel = sirius.get_channel(channel=34)
channel.get_currently_playing()
currentDate = datetime.date.today()
#with open("lithium_" + currentDate.strftime('%d-%m-%y'), "w") as outputFile:
oldSong = ""
outputFile = open("lithium_" + datetime.date.today().strftime('%d-%m-%y'), "w")

while True:
    if (currentDate != datetime.date.today()):
        currentDate = datetime.date.today()
        outputFile.close()
        outputFile = open("lithium_" + datetime.date.today().strftime('%d-%m-%y'), "w")
    channel.get_currently_playing()
    line = ""
    if (channel.currently_playing.artist_name is not None):
        print('artist: ' + str(channel.currently_playing.artist_name))
        line += str(channel.currently_playing.artist_name) + ","
    if (channel.currently_playing.song_name is not None):
        print('song:   ' + str(channel.currently_playing.song_name))
        line += str(channel.currently_playing.song_name) + ","
    if (channel.currently_playing.album is not None):
        print('album: ' + str(channel.currently_playing.album))
        line += str(channel.currently_playing.album) + ","
    if (channel.currently_playing.start is not None):
        print('start: ' + str(channel.currently_playing.start))
        line += str(channel.currently_playing.start) + "\n"
    print(' ')
    print("comparing " + str(oldSong) + " to " + str(channel.currently_playing.song_name))
    if (oldSong != channel.currently_playing.song_name):
        print("New song! Tweeting, and writing to file.")
        message = "Lithium - Now playing: " + str(channel.currently_playing.song_name) + " by " + str(channel.currently_playing.artist_name)
        twitter.update_status(status=message)
        outputFile.write(line)
        outputFile.flush()
        oldSong = channel.currently_playing.song_name
    else:
        print("Same song is still playing...")
    time.sleep(120)
