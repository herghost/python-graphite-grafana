#! /usr/bin/python
import ConfigParser
import requests
import socket
import time
import re
import datetime
import calendar

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
            timestamp = int(time.time())
            tosend = []

            #Stats
            url = "http://" + Config.get('sabnzbd', 'host') + ":" + Config.get('sabnzbd','port') + "/sabnzbd/api?apikey=" + Config.get('sabnzbd', 'token') + "&output=json&mode=server_stats"

            sab = requests.get(url)
            sabout = sab.json()


            week = float(sabout['week'])
            week = float(week / 1073741824)
            week = "%.2f" %week

            total = float(sabout['total'])
            total = float(total / 1073741824)
            total = "%.2f" % total

            day = float(sabout['day'])
            day = float(day / 1073741824)
            day = "%.2f" % day


            tosend.append(Config.get('sabnzbd','statname') + '.download_week %s %d' % (week, timestamp))
            tosend.append(Config.get('sabnzbd','statname') + '.download_total %s %d' % (total, timestamp))
            tosend.append(Config.get('sabnzbd','statname') + '.download_day %s %d' % (day, timestamp))

            servers = sabout["servers"]

            for k , v in servers.items():
                week = float(sabout["servers"][k]['week'])
                week = float(week / 1073741824)
                week = "%.2f" % week

                total = float(sabout["servers"][k]['total'])
                total = float(total / 1073741824)
                total = "%.2f" % total

                day = float(sabout["servers"][k]['day'])
                day = float(day / 1073741824)
                day = "%.2f" % day

                tosend.append(Config.get('sabnzbd','statname') + '.' + k.replace('.','_') + '.download_day %s %d' % (day, timestamp))
                tosend.append(Config.get('sabnzbd','statname') + '.' + k.replace('.','_') + '.download_week %s %d' % (week, timestamp))
                tosend.append(Config.get('sabnzbd','statname') + '.' + k.replace('.','_') + '.download_total %s %d' % (total, timestamp))

            # Downloading
            url = "http://" + Config.get('sabnzbd', 'host') + ":" + Config.get('sabnzbd','port') + "/sabnzbd/api?apikey=" + Config.get('sabnzbd', 'token') + "&output=json&mode=qstatus"
            sab = requests.get(url)
            sabout = sab.json()

            tosend.append(Config.get('sabnzbd','statname') + '.downloading_count %s %d' % (sabout["noofslots"], timestamp))

            speed = re.sub("[^0-9]","",sabout["speed"])
            tosend.append(Config.get('sabnzbd','statname') + '.downloading_speed %s %d' % (speed, timestamp))

            mb = sabout["mbleft"]
            tosend.append(Config.get('sabnzbd', 'statname') + '.downloading_remain %s %d' % (mb, timestamp))


            message =  '\n'.join(tosend) + '\n'
            send(message)
            time.sleep(Config.getfloat('sabnzbd', 'delay'))