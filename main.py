from slacker import Slacker
import websocket
import functools32 as functools
import thread
import time
import json
import sys
import basic_logger

L = basic_logger.Logger("main")

@functools.lru_cache(maxsize=16)
def get_api_token():
    with open("api_token.txt", "r") as f:
        token = f.read().rstrip("\n")
        return token

@functools.lru_cache(maxsize=16)
def get_channel_id(slack, channel_name):
    r = slack.channels.list()
    channel_id_map = {}
    for channel in r.body["channels"]:
        if channel["name"] == channel_name:
            L.info("Channel ID for channel %s is %s" % (channel_name, channel["id"]))
            return channel["id"]
    L.warn("No channel ID for name: %s" % channel_name)

@functools.lru_cache(maxsize=16)
def get_channel_name(slack, channel_id):
    r = slack.channels.list()
    channel_id_map = {}
    for channel in r.body["channels"]:
        if channel["id"] == channel_id:
            L.info("Channel name for ID %s is %s" % (channel_id, channel["name"]))
            return channel["id"]
    L.warn("No channel name for ID: %s" % channel_name)

@functools.lru_cache(maxsize=16)
def get_user_id(slack, user_name):
    r = slack.users.list()
    for item in r.body["members"]:
        if item["name"] == user_name:
            return item["id"]
    L.warn("No user ID for name: %s" % user_name)

@functools.lru_cache(maxsize=16)
def get_user_name(slack, user_id):
    r = slack.users.list()
    for item in r.body["members"]:
        if item["id"] == user_id:
            return item["name"]
    L.warn("No username for ID: %s" % user_id)

def is_targeted_message(slack, user_name, message):
    uid = get_user_id(slack, user_name)
    mention = "<@%s>" % uid
    return "text" in message and mention in message["text"]

def generate_reply(slack, channel_id):
    obj = {
        "id": 1,
        "type": "message",
        "channel": channel_id,
        "text": "'Sup groots",
    }
    return json.dumps(obj)

def decode_message(msg_text):
    return json.loads(msg_text)

def on_message(ws, msg_text, slack):
    message = decode_message(msg_text)
    print message
    if is_targeted_message(slack, "questionbot", message):
        L.info("Got message from user %s" % get_user_name(slack, message["user"]))
        ws.send(generate_reply(slack, message["channel"]))

def on_error(ws, error, slack):
    L.error("Got a slack error: %s" % error)

def on_close(ws, slack):
    L.warn("Connection closed")

def on_open(ws, slack):
    L.info("Connection opened")

def main():
    L.info("Starting QuestionBot")
    slack = Slacker(get_api_token())
    r = slack.rtm.start()
    url = r.body["url"]
    L.info("WS URL: %s" % url)

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url,
            on_message = lambda ws,msg: on_message(ws, msg, slack),
            on_error = lambda ws,msg: on_error(ws, error, slack),
            on_close = lambda ws: on_close(ws, slack))
    ws.on_open = lambda ws: on_open(ws, slack)
    ws.run_forever()

if __name__ == "__main__":
    main()
