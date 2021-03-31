
# work around quirks in paho.mqtt.client to reconnect
# under all conditions

import sondehub
import json
import time

interval = 5
restart_after_silence = 30
msgs = 0
elapsed = 0
starttime = 0
sh = None
lastheard = 0
log = False

def now():
    return int(time.time())

def on_msg(*args):
    global msgs
    msgs +=1
    global lastheard
    lastheard = now()

def on_connect(*args):
    global starttime
    elapsed = now() - starttime
    print(f"on_connect at {elapsed=}", *args)

def on_disconnect(*args):
    print(f"on_disconnect at {now()}", *args)

def on_log(*args):
    if log:
        print(f"on_log at {now()}: ", *args)
   
starttime = now()
lastheard = now()

while True:
    if sh is None or lastheard + restart_after_silence < now() or sh.connected is False:
        try:
            print(f"instantiate")
            sh  = sondehub.Stream(on_message=on_msg,
                                  on_disconnect=on_disconnect,
                                  on_log=on_log,
                                  on_connect=on_connect);
        except Exception as e:
            print(f" {e=}")
            # paho goes deaf on exceptions
            sh = None
            
    time.sleep(interval)
    elapsed = now() - starttime
    print(f"tick at {elapsed=} {msgs=}")
    msgs = 0
