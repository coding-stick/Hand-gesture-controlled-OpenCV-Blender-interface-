import socket, math
import json
import time
from config import *
from tracking import HandTracker
from funcs import *

HOST = '127.0.0.1'
PORT = 65432

tracker = HandTracker()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    print("Connected to Blender server, starting data transmission...")
    while True:
        tracker.run()
        zoom = int(zoom_func(tracker.zoom))
        rotation = rot_func(tracker.rotation).tolist()
        translation = trans_func(tracker.translate).tolist()
        #print(rotation, translation, zoom)

        data = {
            "zoom": zoom,
            "rotation": rotation,
            "translation": translation
        }

        s.sendall(json.dumps(data).encode())
        time.sleep(0.05)
