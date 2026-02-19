import bpy
import socket
import threading
import json

HOST = '127.0.0.1'
PORT = 65432
print("starting....")
def update_object(data):
    print(data)
    obj = bpy.data.objects["Cube"]  # change to your object name
    
    obj.location = data["translation"]
    obj.rotation_euler = data["rotation"]
    obj.scale = (data["zoom"], data["zoom"], data["zoom"])



def socket_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print("Server listening...")

        while True:  # <- stay alive forever
            print("Waiting for connection...")
            conn, addr = s.accept()
            print("Connected:", addr)

            with conn:
                while True:
                    try:
                        data = conn.recv(1024)
                        if not data:
                            print("Client disconnected")
                            break

                        values = json.loads(data.decode())
                        bpy.app.timers.register(
                            lambda v=values: update_object(v),
                            first_interval=0.0
                        )

                    except Exception as e:
                        print("Connection error:", e)
                        break

threading.Thread(target=socket_server, daemon=True).start()
