import asyncio
import websockets
import json

debug_print = True


def default_handler(type, data):
    print(type)


on_move = {
    "WaitingForOpponent": default_handler,
    "ReadyToStart": default_handler,
    "board": default_handler,
    "IllegalMove": default_handler
}


def process(data):
    if data['type'] in on_move.keys():
        on_move[data['type']](data['type'], data)


async def hello():
    async with websockets.connect('ws://localhost:9000/join') as websocket:
        global debug_print

        # wait for opponent
        message = await websocket.recv()
        if debug_print:
            print("< {}".format(message))

        while True:
            message = await websocket.recv()
            if debug_print:
                print("< {}".format(message))

            data = json.loads(message)
            # print(data)
            process(data)

            name = input("please input move:")
            await websocket.send(name)
            if debug_print:
                print("> {}".format(name))


asyncio.get_event_loop().run_until_complete(hello())
