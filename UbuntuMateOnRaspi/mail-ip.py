#!/usr/bin/python
import socket
import fcntl
import struct
from socket import gaierror
import string
import smtplib
import time

# This script attepts to retrieve the IP address of a specified interface.
# If successful it then emails the retrieved IP to a specified email address

#	FILL OUT THE VALUES BETWEEN THE COMMENT BLOCKS
#######################################################################
# Specify the sender credentials and recipient email address here
SENDER = {}
SENDER['addr'] = '1740701729@qq.com' 
SENDER['pass'] = 'zibpgmnvhaqjbjgi'
SENDER['serv'] = 'smtp.qq.com'
SENDER['port'] = 465  # default SMTP port

RECEIVER = {}
RECEIVER['addr'] = [ '78512379@qq.com' ]; 
# Note: RECEIVER['addr']  must be a list (ie don't delete the brackets)!
# This allows the specification of a list of addresses ['me@addr.com', 'you@addr.com', 'them@addr.com']

# specify the interface to query
INTERFACE = 'wlan0' # default interface for a Raspberry Pi

RETRY_TIMES = 5
RETRY_INTERVALS = 10    # Retry intervals in seconds

#######################################################################
def get_local_ip(interface):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915, # SIOCGIFADDR
            struct.pack('256s', interface[:15])
        )[20:24])
    except Exception as e:
        return 'no address found'

def save_ip_to_cache(path, ip):
    cache_file = None
    try:
        cache_file = open(path, 'w')
        cache_file.write(ip)
    except Exception as e:
        print(e)
    finally:
        if cache_file is not None:
            cache_file.close()

def load_ip_from_cache(path):
    ip = ''
    cache_file = None
    try:
        cache_file = open(path, 'r')
        lines = cache_file.readlines()
        if len(lines) > 0:
            ip = lines[0]
    except Exception as e:
        print(e)
    finally:
        if cache_file is not None:
            cache_file.close()
    return ip 

#######################################################################

CACHE_FILE = '/tmp/%s.ip' % INTERFACE

retry_times = 0
last_ip = load_ip_from_cache(CACHE_FILE)

while True:
    the_ip = get_local_ip(INTERFACE)
    save_ip_to_cache(CACHE_FILE, the_ip)

    if the_ip == 'no address found':
        print('no address found...')
        if retry_times < RETRY_TIMES:
            time.sleep(RETRY_INTERVALS) # Waitting for retry
            retry_times += 1
        else:
            break
    elif the_ip != last_ip:
        SUBJECT = "%s's IP:%s on:%s" % ('dk-desktop', the_ip, INTERFACE)

        # Construct the Email
        TO = RECEIVER['addr']
        FROM = SENDER['addr'] 
        BODY = string.join((
            'From: %s' % FROM,
            'To: %s' % TO,
            'Subject: %s' % SUBJECT,
            '',
            ''
            ), '\r\n')

        # Try to send the email
        try:
            server = smtplib.SMTP_SSL( SENDER['serv'], SENDER['port'] )     # NOTE:  This is the QQ SSL port.
            server.login( SENDER['addr'], SENDER['pass'] )
            server.sendmail( FROM, TO, BODY )
            server.quit()

        except smtplib.SMTPAuthenticationError:
            print "Error, authentication failed! Please check your username and password."

        except gaierror:
            print 'Error, cannot connect to: %s!  Please ensure it is a valid smtp server.' %(SENDER['serv'])

        print(SUBJECT)
        break
    else:
        print('IP not changed')
        break
