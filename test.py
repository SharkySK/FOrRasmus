#!/usr/bin/env python

import signal
import time
import sys

from pirc522 import RFID

run = True
logged = False
rdr = RFID()
util = rdr.util()
util.debug = True
last = 0
start = 0


def end_read(signal,frame):
    global run
    print("\nCtrl+C captured, ending read.")
    run = False
    rdr.cleanup()
    sys.exit()


signal.signal(signal.SIGINT, end_read)
print("Starting")

while run:
    rdr.wait_for_tag()

    (error, data) = rdr.request()
    if not error:
        print("\nDetected: " + format(data, "02x"))

    (error, uid) = rdr.anticoll()
    if not error:
        print("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
        if logged:
            if not uid == last:
                break
            else:
                total = (time.time() - start)
                print("Total time: " + total)
                logged = False
        else:
            start = time.time()
            logged = True
            last = uid
        time.sleep(1)
