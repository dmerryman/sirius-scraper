from pysosirius import PySoSirius
from time import sleep
import datetime
from twython import Twython
from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)
from song_titles_to_ignore import(
    ignored_songs
)
from alt8 import(
    alt_8
)


sirius = PySoSirius()
twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

channel = sirius.get_channel(channel=36)
channel.get_currently_playing()
currentDate = datetime.date.today()
#with open("lithium_" + currentDate.strftime('%d-%m-%y'), "w") as outputFile:
oldSong = ""
outputFile = open("altnation_" + datetime.date.today().strftime('%d-%m-%y'), "w")
tweetNextSong = False
top8Position = ""


while True:
    if (currentDate != datetime.date.today()):
        currentDate = datetime.date.today()
        outputFile.close()
        outputFile = open("lithium_" + datetime.date.today().strftime('%d-%m-%y'), "w")
    channel.get_currently_playing()
    sleep(1)
    if channel.currently_playing.song_name is not None:
        currentSong = str(channel.currently_playing.song_name)
        currentArtist = str(channel.currently_playing.artist_name)
        currentAlbum = str(channel.currently_playing.album)
        currentStartTime = str(channel.currently_playing.start)
        if (currentSong.lower() not in ignored_songs):
            line = currentArtist + "," + currentSong + "," + currentAlbum + "," + currentStartTime + "\n"
            if (oldSong != currentSong):
                message = "Alt Nation - Now playing: " + currentSong + " by " + currentArtist + ". " 
                print(message + " writing to file.")
                #twitter.update_status(status=message)
                if (currentSong.lower() in alt_8):
                    tweetNextSong = True
                    top8Position = currentSong
                else:
                    tweetNextSong = False
                if (tweetNextSong == True):
                    message = top8Position + " " + currentSong + " by " + currentArtist
                    twitter.update_status(status=message)
                outputFile.write(line)
                outputFile.flush()
                oldSong = currentSong
                sleep(3)
            else:
                print("same song is still playing. ignoring")
                sleep(3)
        else:
            print("Ignoring " + currentSong)
            sleep(3)
    else:
        sleep(3)
