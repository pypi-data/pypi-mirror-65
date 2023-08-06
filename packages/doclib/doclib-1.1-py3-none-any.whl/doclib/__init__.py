import websockets
import websocket
import json
import re
import random
import argparse
from attrdict import AttrDict
import attrdict
from getpass import getpass




class Bot:
    def __init__(self, nick, room = "bots", owner = None, password = "", help = None, ping = None, important = False, killed = None, API_timeout = 10):
        parser = argparse.ArgumentParser(description=f'{nick}: A euphoria.io bot.')
        parser.add_argument("--test", "--debug", "-t", help = "Used to debug dev builds. Sends bot to &test instead of its default room.", action = 'store_true')
        parser.add_argument("--room", "-r", help = f"Set the room the bot will be placed in. Default: {room}", action = "store", default = room)
        parser.add_argument("--password", "-p", help = "Set the password for the room the bot will be placed in.", action = "store", default = password)

        args = parser.parse_args()

        self.nick = nick
        self.room = args.room if args.test != True else "test"
        print("Debug: " + str(args.test))
        self.normname = re.sub(r"\s+", "", self.nick)
        self.owner = owner if owner != None else "nobody"
        self.normowner = re.sub(r"\s+", "", self.owner)
        self.password = args.password
        self.handlers = {}
        self.help = help
        self.ping = ping
        self.important = important
        self.killed = killed
        self.API_timeout = API_timeout


    def connect(self):
        self.conn = websocket.create_connection(f'wss://euphoria.io/room/{self.room}/ws')
        self.conn.recv()
        reply = AttrDict(json.loads(self.conn.recv()))
        self.handle_ping(reply)
        reply = AttrDict(json.loads(self.conn.recv()))
        if reply.type == "snapshot-event":
            self.setNick(self.nick)
        elif reply.type == "bounce-event":
            self.handle_auth(self.password)
            self.setNick(self.nick)
        else:
            print(reply)
        print(f'connected to &{self.room}.')

    def sendMsg(self, msgString, parent = None):
        if re.search(r"^\[.+,.+\]$", msgString):
            msgString = random.choice(msgString[1:-1].split(","))
        if isinstance(parent, AttrDict):
            self.conn.send(json.dumps({'type': 'send', 'data': {'content': msgString, 'parent': parent.data.id}}))
            reply = None
            i = 0
            for msgJSON in self.conn:
                i += 1
                msg = AttrDict(json.loads(msgJSON))
                if msg.type == "send-reply":
                    reply = msg
                    print(f'Message sent: {reply} replying to: {parent.data.id} by {parent.data.sender.name}')
                    return reply
                if i > self.API_timeout:
                    print("send-reply API response not recorded. reason: too many events before send-reply.")
                    return None

        elif isinstance(parent, str):
            self.conn.send(json.dumps({'type': 'send', 'data': {'content': msgString, 'parent': parent}}))
            reply = None
            i = 0
            for msgJSON in self.conn:
                i += 1
                msg = AttrDict(json.loads(msgJSON))
                if msg.type == "send-reply":
                    reply = msg
                    print(f'Message sent: {reply} replying to: {parent}')
                    return reply
                if i > self.API_timeout:
                    print("send-reply API response not recorded. reason: too many events before send-reply.")
                    return None

        else:
            raise BadMessageError(f'message not sent, because type of parent was {type(parent)}').with_traceback(f'parent = {parent}')




    def restart(self, msg = None):
        self.conn.close()
        self.connect()
        self.start()
        self.sendMsg("Restarted", parent = msg)

    def simple_start(self):
        try:
            for msgJSON in self.conn:
                msg = AttrDict(json.loads(msgJSON))
                if msg.type == 'ping-event':
                    self.handle_ping(msg)
                elif msg.type == 'send-event' and msg.data.sender.name != self.nick:
                    self.handle_message(msg)
                elif msg.type == 'error':
                    print(msg)
                elif msg.type == 'bounce-event':
                    self.handle_auth(msg)
                else:
                    self.handle_other(msg)
        except KilledError:
            pass

    def nothing(msg):
        return

    def is_privileged(self, user):
        if "is_manager" in user.keys() or user.name == self.owner:
            return True
        else:
            return False

    def set_regexes(self, regexes):
        self._regexes = regexes
        if self.help == None:
            if f"^!help @{self.normname}$" in regexes.keys():
                self.help = regexes[f"^!help @{self.normname}$"]
            else:
                self.help = f"@{self.normname} is a bot made with Doctor Number Four's Python 3 bot library, DocLib (link: https://github.com/milovincent/DocLib) by @{self.normowner}.\nIt follows botrulez and does not have a custom !help message yet."
        if self.ping == None:
            if '^!ping$' in regexes.keys():
                self.ping = regexes['^!ping$']
            elif f'^!ping @{self.normname}$' in regexes.keys():
                self.ping = regexes[f'^!ping @{self.normname}$']
            else:
                self.ping = "Pong!"
        if self.killed == None:
            if f"^!kill @{self.normname}$" in regexes.keys():
                self.killed = regexes[f"^!kill @{self.normname}$"]
            else:
                self.killed = "/me has died."

    def advanced_start(self, function = nothing):
        if callable(function):
            try:
                for msgJSON in self.conn:
                    msg = AttrDict(json.loads(msgJSON))
                    if msg.type == 'send-event' and msg.data.sender.name != self.nick:
                        if re.search(f'^!kill @{self.normname}$', msg.data.content) != None:
                            self.handle_kill(msg)
                        if re.search(f'^!forcekill @{self.normname}$', msg.data.content) != None:
                            self.kill()
                        if re.search(f'^!restart @{self.normname}$', msg.data.content) != None:
                            self.restart()
                    if msg.type in self.handlers.keys():
                        self.handlers[msg.type](msg)
                    else:
                        self.function(msg)
            except KilledError:
                pass
        else:
            print("Advanced start must be given a callable message handler function that takes an AttrDict as its argument.")

    def handle_ping(self, msg):
        self.conn.send(json.dumps({'type': 'ping-reply', 'data': {'time': msg.data.time}}))

    def handle_message(self, msg):
        if re.search(f'^!kill @{self.normname}$', msg.data.content) != None:
            self.handle_kill(msg)
        if re.search(f'^!forcekill @{self.normname}$', msg.data.content) != None:
            self.kill()
        if re.search(f'^!restart @{self.normname}$', msg.data.content) != None:
            self.restart()
        if re.search('^!ping$', msg.data.content) != None or re.search(f'^!ping @{self.normname}$', msg.data.content) != None:
            self.sendMsg(self.ping, parent = msg)
        if re.search(f'^!help @{self.normname}$', msg.data.content) != None:
            self.sendMsg(self.help, parent = msg)
        for regex, response in self._regexes.items():
            if re.search(regex, msg.data.content) != None:
                if callable(response):
                    result = response(self, msg)
                    if type(result) == str:
                        self.sendMsg(result, parent = msg)
                    elif type(result) == dict:
                        for send, nick in result.items():
                            self.setNick(nick)
                            self.sendMsg(send, parent = msg)
                        self.setNick(self.nick)
                    elif type(result) == list:
                        for send in result:
                            self.sendMsg(send, parent = msg)
                else:
                    self.sendMsg(response, parent = msg)
                break

    def handle_kill(self, msg):
        if self.is_privileged(msg.data.sender) or not self.important:
            self.sendMsg(self.killed, msg)
            self.kill()
        else:
            self.sendMsg(f"Bot not killed because you are not a host or @{self.normowner}, and this bot is marked as important.\nFor emergencies, use !forcekill.", parent = msg)

    def handle_auth(self, pw):
        self.conn.send(json.dumps({'type': 'auth', 'data': {'type': 'passcode', 'passcode': pw}}))
        reply = None
        i = 0
        for msgJSON in self.conn:
            i += 1
            msg = AttrDict(json.loads(msgJSON))
            if msg.type == "auth-reply":
                reply = msg
                if reply.data.success == True:
                    print(f'Successfully logged into {self.room}.')
                else:
                    print(f'Login unsuccessful. Reason: {reply.data.reason}')
                    self.handle_auth(getpass("Enter the correct password: "))
                break
            if i > self.API_timeout:
                print("Auth Error: auth-reply API response not recorded.")
                break

    def handle_other(self, msg):
        if msg.type in self.handlers.keys():
            self.handlers[msg.type](msg)


    def setNick(self, nick):
        self.conn.send(json.dumps({'type': 'nick', 'data': {'name': nick}}))

    def kill(self):
        self.conn.close()
        raise KilledError(f'{self.normname} killed.')

    def get_userlist(self):
        self.conn.send(json.dumps({'type': 'who', 'data': {}}))
        reply = None
        i = 0
        for msgJSON in self.conn:
            i += 1
            msg = AttrDict(json.loads(msgJSON))
            if msg.type == "who-reply":
                reply = msg
                print(f'Message sent: {reply} replying to: {parent.data.id} by {parent.data.sender.name}')
                return reply.data.listing
            if i > self.API_timeout:
                print("who-reply API response not recorded. reason: too many events before who-reply.")
                return None


    def move_to(self, roomName, password = ""):
        self.room = roomName
        self.password = password
        self.restart()

    def set_handler(self, eventString, function):
        if callable(function):
            self.handlers += {eventString : function}
        else:
            print(f"WARNING: handler for {eventString} not callable, handler not set.")

class BotError(Exception):
    pass

class KilledError(BotError):
    def __init__(self, message = "bot killed."):
        self.message = message
        print(f'KilledError: {message}')

class BadMessageError(BotError):
    def __init__(self, message):
        self.message = message
        print(f'BadMessageError: {message}')
