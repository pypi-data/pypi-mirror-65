import websockets
import websocket
import json
import re
import random
import argparse
import sys
from attrdict import AttrDict
import attrdict
from getpass import getpass


def botlog(message, error = False):
    ERROR = "\033[1;31;40m"
    NORMAL = "\033[m"
    print((ERROR if error else NORMAL) + message + NORMAL)
    sys.stdout.flush()

class Bot:


    def __init__(self, nick, room = "bots", owner = None, password = "", help = None, ping = None, important = False, killed = None, API_timeout = 10, advanced = False, function = None, sendable = False):
        parser = argparse.ArgumentParser(description=f'{nick}: A euphoria.io bot.')
        parser.add_argument("--test", "--debug", "-t", help = "Used to debug dev builds. Sends bot to &test instead of its default room.", action = 'store_true')
        parser.add_argument("--room", "-r", help = f"Set the room the bot will be placed in. Default: {room}", action = "store", default = room)
        parser.add_argument("--password", "-p", help = "Set the password for the room the bot will be placed in.", action = "store", default = password)

        args = parser.parse_args()

        self.nick = nick
        self.room = args.room if args.test != True else "test"
        botlog("Debug: " + str(args.test))
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
        self.advanced = advanced
        self.function = function
        self.sendable = sendable


    def connect(self):
        self.conn = websocket.create_connection(f'wss://euphoria.io/room/{self.room}/ws')
        self.conn.recv()
        reply = AttrDict(json.loads(self.conn.recv()))
        self._handle_ping(reply)
        reply = AttrDict(json.loads(self.conn.recv()))
        if reply.type == "snapshot-event":
            self.set_nick(self.nick)
        elif reply.type == "bounce-event":
            self._handle_auth(self.password)
            self.set_nick(self.nick)
        else:
            botlog(reply, error = True)
        botlog(f'connected to &{self.room}.')

    def send_msg(self, msgString, parent = None):
        if re.search(r"^\[.+,.+\]$", msgString):
            msgString = random.choice(msgString[1:-1].split(","))
        try:
            if isinstance(parent, AttrDict):
                self.conn.send(json.dumps({'type': 'send', 'data': {'content': msgString, 'parent': parent.data.id}}))
                reply = None
                i = 0
                for msgJSON in self.conn:
                    i += 1
                    msg = AttrDict(json.loads(msgJSON))
                    if msg.type == "send-reply":
                        reply = msg
                        botlog(f'Message sent: {reply} replying to: {parent.data.id} by {parent.data.sender.name}')
                        return reply
                    if i > self.API_timeout:
                        botlog("send-reply API response not recorded. reason: too many events before send-reply.", True)
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
                        botlog(f'Message sent: {reply} replying to: {parent}')
                        return reply
                    if i > self.API_timeout:
                        botlog("send-reply API response not recorded. reason: too many events before send-reply.", True)
                        return None

            else:
                raise BadMessageError(f'message not sent, because type of parent was {type(parent)}. \nParent printed: \n{parent}')
        except BadMessageError:
            pass




    def restart(self, msg = None):
        self.conn.close()
        del self.conn
        botlog("restarting...")
        self.connect()
        self.start()
        self.send_msg("Restarted", parent = msg)

    def nothing(msg):
        return

    def start(self, function = None, advanced = False):
        if not (self.advanced or advanced):
            try:
                for msgJSON in self.conn:
                    msg = AttrDict(json.loads(msgJSON))
                    if msg.type == 'ping-event':
                        self._handle_ping(msg)
                    elif msg.type == 'send-event' and msg.data.sender.name != self.nick:
                        self._handle_message(msg)
                    elif msg.type == 'error':
                        botlog(msg, error = True)
                    elif msg.type == 'bounce-event':
                        self._handle_auth(msg)
                    else:
                        self._handle_other(msg)
            except KilledError:
                pass
        else:
            if self.function == None and function != None and callable(function):
                self.function = function
            else:
                botlog("No function passed to advanced bot's start function.")
            try:
                for msgJSON in self.conn:
                    msg = AttrDict(json.loads(msgJSON))
                    if msg.type == 'send-event' and msg.data.sender.name != self.nick:
                        if re.search(f'^!kill @{self.normname}$', msg.data.content) != None:
                            self._handle_kill(msg)
                        if re.search(f'^!forcekill @{self.normname}$', msg.data.content) != None:
                            self.kill()
                        if re.search(f'^!restart @{self.normname}$', msg.data.content) != None:
                            self.restart(msg = msg)
                    if msg.type in self.handlers.keys():
                        self.handlers[msg.type](msg)
                    else:
                        if function != None and callable(function):
                            function(msg)
                        elif callable(self.function):
                            self.function(msg)
                        else:
                            botlog("Advanced start must be given a callable message handler function that takes an AttrDict as its argument.", error = True)
            except KilledError:
                pass



    def _is_privileged(self, user):
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

    def _handle_ping(self, msg):
        self.conn.send(json.dumps({'type': 'ping-reply', 'data': {'time': msg.data.time}}))

    def _handle_message(self, msg):
        if re.search(f'^!kill @{self.normname}$', msg.data.content) != None:
            self._handle_kill(msg)
        if re.search(f'^!forcekill @{self.normname}$', msg.data.content) != None:
            self.kill()
        if re.search(f'^!restart @{self.normname}$', msg.data.content) != None:
            self.restart()
        if re.search('^!ping$', msg.data.content) != None or re.search(f'^!ping @(?i){self.normname}$', msg.data.content) != None:
            self.send_msg(self.ping, parent = msg)
        if re.search(f'^!help @(?i){self.normname}$', msg.data.content) != None:
            self.send_msg(self.help, parent = msg)
        if re.search(f'^!send @(?i){self.normname} &(\w+)$', msg.data.content) != None and self.sendable:
            self.move_to(re.search(f'^!send @(?i){self.normname} &(\w+)$', msg.data.content).group(0))
        for regex, response in self._regexes.items():
            if re.search(regex, msg.data.content) != None:
                if callable(response):
                    result = response(self, msg, re.search(regex, msg.data.content))
                    if type(result) == str:
                        self.send_msg(msgString = result, parent = msg)
                    elif type(result) == dict:
                        for send, nick in result.items():
                            self.set_nick(nick)
                            self.send_msg(send, parent = msg)
                        self.set_nick(self.nick)
                    elif type(result) == list:
                        for send in result:
                            self.send_msg(send, parent = msg)
                else:
                    self.send_msg(response, parent = msg)
                break

    def _handle_kill(self, msg):
        if self._is_privileged(msg.data.sender) or not self.important:
            self.send_msg(self.killed, msg)
            self.kill()
        else:
            self.send_msg(f"Bot not killed because you are not a host or @{self.normowner}, and this bot is marked as important.\nFor emergencies, use !forcekill.", parent = msg)

    def _handle_auth(self, pw):
        self.conn.send(json.dumps({'type': 'auth', 'data': {'type': 'passcode', 'passcode': pw}}))
        reply = None
        i = 0
        for msgJSON in self.conn:
            i += 1
            msg = AttrDict(json.loads(msgJSON))
            if msg.type == "auth-reply":
                reply = msg
                if reply.data.success == True:
                    botlog(f'Successfully logged into {self.room}.')
                else:
                    botlog(f'Login unsuccessful. Reason: {reply.data.reason}', error = True)
                    self._handle_auth(getpass("Enter the correct password: "))
                break
            if i > self.API_timeout:
                botlog("Auth Error: auth-reply API response not recorded.", error = True)
                break

    def _handle_other(self, msg):
        if msg.type in self.handlers.keys():
            self.handlers[msg.type](msg)


    def set_nick(self, nick):
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
                return reply.data.listing
            if i > self.API_timeout:
                botlog("who-reply API response not recorded. reason: too many events before who-reply.", error = True)
                return None


    def move_to(self, roomName, password = ""):
        self.room = roomName
        self.password = password
        self.restart()

    def set_handler(self, eventString, function):
        if callable(function):
            self.handlers += {eventString : function}
        else:
            botlog(f"WARNING: handler for {eventString} not callable, handler not set.", error = True)

class BotError(Exception):
    pass

class KilledError(BotError):
    def __init__(self, message = "bot killed."):
        self.message = message
        botlog(f'KilledError: {message}', error = True)

class BadMessageError(BotError):
    def __init__(self, message):
        self.message = message
        botlog(f'BadMessageError: {message}', error = True)
