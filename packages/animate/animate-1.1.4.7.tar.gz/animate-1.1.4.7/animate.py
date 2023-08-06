#coding: utf-8
import itertools
import threading
import time
import sys
import os
anim_stop=False
start_stop=False

stop = False
def animate(stop):
    global anim_stop
    for c in itertools.cycle(['\x1b[1;31m•    \x1b[1;36m|', '\x1b[1;32m••   \x1b[1;36m/', '\x1b[1;34m•••  \x1b[1;36m-', '\x1b[1;35m•••• \x1b[1;36m\\']):
	if anim_stop == True:
           anim_stop = False
	   break
	else:
	   sys.stdout.write('\r\x1b[1;32mloading ' + c)
           sys.stdout.flush()
           time.sleep(0.2)

def star(text):
    global start_stop
    text = text.upper()
    teln = len(text) - 1
    lo = 0
    while True:
      if start_stop == True:
         start_stop = False
	 print("\n")
         break
      else:
         tek = text[:lo] + text[lo].swapcase() + text[lo+1:]
         sys.stdout.write("\r\x1b[1;32m[+]\x1b[1;33m "+tek)
         sys.stdout.flush()
         time.sleep(0.2)
         lo -=-1
         if lo > teln:
            lo = 0
    print("\n")

def start(tup):
	t = threading.Thread(target=star,args=(tup,))
        t.daemon = True
        t.start()

def anim():
    b = threading.Thread(target=animate,args=(stop,))
    b.daemon = True
    b.start()


anim()
time.sleep(3)
anim_stop=True
