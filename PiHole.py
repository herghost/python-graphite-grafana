
#! /usr/bin/python
#Thanks to https://fattylewis.com/Graphing-pi-hole-stats/ for the inspiration and base for this script
import ConfigParser
import requests
import socket
import time



Config = ConfigParser.ConfigParser()
Config.read("config.ini")

CarbonHost = Config.get('carbon', 'host')
CarbonPort = Config.getint('carbon', 'port')

Delay = Config.get('pihole','delay')

def send(message):
    sock = socket.socket()
    sock.connect((CarbonHost,CarbonPort))
    sock.sendall(message)
    sock.close()

if __name__ == '__main__':
    while True:
        api  = requests.get("http://" + Config.get('pihole','host') + "/admin/api.php")
        api_out = api.json()

        domains_blocked = (api_out['domains_being_blocked']).replace(',','')
        dns_queries_today = (api_out['dns_queries_today']).replace(',','')
        ads_percentage_today = (api_out['ads_percentage_today']).replace(',','')
        ads_blocked_today = (api_out['ads_blocked_today']).replace(',','')

        timestamp = int(time.time())

        tosend = [
            'pihole.%s.domains_blocked %s %d' % (Config.get('pihole','statname'), domains_blocked, timestamp),
            'pihole.%s.dns_queries_today %s %d' % (Config.get('pihole','statname'), dns_queries_today, timestamp),
            'pihole.%s.ads_percentage_today %s %d' % (Config.get('pihole','statname'), ads_percentage_today, timestamp),
            'pihole.%s.ads_blocked_today %s %d' % (Config.get('pihole','statname'), ads_blocked_today, timestamp),
        ]

        message = '\n'.join(tosend) + '\n'
        send(message)
        time.sleep(Config.getfloat('pihole','delay'))













