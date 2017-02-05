#! /usr/bin/python

#! /usr/bin/python
import ConfigParser
import requests
import socket
import time

Config = ConfigParser.ConfigParser()
Config.read("config.ini")

CarbonHost = Config.get('carbon', 'host')
CarbonPort = Config.getint('carbon', 'port')

Delay = Config.get('plex','delay')

def send(message):
    sock = socket.socket()
    sock.connect((CarbonHost,CarbonPort))
    sock.sendall(message)
    sock.close()

if __name__ == '__main__':
    while True:
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

            tosend.append(Config.get('plex','statname') + '.ondeck_count %s %d' % (items_on_deck, timestamp))
            tosend.append(Config.get('plex','statname') + '.now_playing_count %s %d' % (nowplayingcount, timestamp))

            message =  '\n'.join(tosend) + '\n'
            send(message)
            time.sleep(Config.getfloat('plex', 'delay'))



