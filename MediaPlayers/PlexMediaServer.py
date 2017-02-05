#! /usr/bin/python


import ConfigParser
import requests
import socket
import time
import platform
import urllib


Config = ConfigParser.ConfigParser()
Config.read("../config.ini")

CarbonHost = Config.get('carbon', 'host')
CarbonPort = Config.getint('carbon', 'port')

Delay = Config.get('plex','delay')

def send(message):
    sock = socket.socket()
    sock.connect((CarbonHost,CarbonPort))
    sock.sendall(message)
    sock.close()

if __name__ == '__main__':

            headers = {'X-Plex-Token': Config.get('plex', 'token'), 'Accept': 'application/json'}
            timestamp = int(time.time())
            tosend = []

            #On Deck
            url = "http://" + Config.get('plex', 'host') + ":" + Config.get('plex','port') + "/library/onDeck"
            ondeck = requests.get(url,headers = headers)
            ondeckout = ondeck.json()
            items_on_deck = (ondeckout["MediaContainer"]["size"])


            #Now Playing
            url = "http://" + Config.get('plex', 'host') + ":" + Config.get('plex', 'port') + "/status/sessions"
            nowplaying = requests.get(url, headers = headers)
            nowplayingout = nowplaying.json()
            nowplayingcount = nowplayingout['MediaContainer']["size"]

            tosend.append('plex.ondeck_count %s %d' % (items_on_deck, timestamp))
            tosend.append('plex.now_playing_count %s %d' % (nowplayingcount, timestamp))

            message =  '\n'.join(tosend) + '\n'
            send(message)



