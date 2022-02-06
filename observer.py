import socketio

sio = socketio.AsyncClient(logger=True)


@sio.event
def connect():
    print("Connected")


@sio.event
async def disconnect():
    print("connection closed")


@sio.event
async def welcome(data):
    await sio.emit(
        "loaded", {"height": 1080, "width": 1920, "scale": 2, "success": 1}
    )
    await sio.sleep(1.2)
    await sio.disconnect()


# await sio.connect("wss://eud1.adventure.land:2053")
# await sio.wait()
class Observer:
    pass
