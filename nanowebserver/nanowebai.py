# -*- coding: utf-8 -*-

import socket
from datetime import datetime
from os import environ  # VUPPY_IP, VUPPY_PORT, VUPPY_LMBYTES
from colorama import Fore
from colorama import init as cinit
from json import loads

cinit()

DEFAULT_BYTESLIMIT = 56000000  # bytes
DEFAULT_SERVERIP = "127.0.0.1"
DEFAULT_SERVERPORT = 8787

def test(data):
    return 'AI replies "Hello!"'


func = test


class NanoWeb:
    def __init__(self, func):
        """
        Example:

        def io(data):
            return 'AI replies "Hello!"'

        NanoWeb(io) #Start server
        """
        globals()["func"] = func
        init()


class Serv:
    header = "\r\nAccess-Control-Allow-Origin: *\r\nConnection: close\r\nContent-Type: text/plain\r\nContent-Length: "

    def __init__(self, port=DEFAULT_SERVERPORT, bytes_limit=DEFAULT_BYTESLIMIT, listen=1, ip=DEFAULT_SERVERIP):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.bind((ip, port))
        self.soc.listen(listen)
        self.bytes_limit = bytes_limit
        self.connections = 0

    def start(self):
        log("Очікуємо підключення...", msgType="system")
        while 1:
            client, addr = self.soc.accept()
            print("Connection №" + str(self.connections) + Fore.RED + " {" + Fore.RESET)
            log("Підключено: " + addr[0], tabs=2)
            received = b''
            while 1:
                bytes = 65495
                data = client.recv(bytes)
                received += data
                if data.endswith(b"}") and b"\r\n\r\n{" in received:
                    break
                if len(received) >= self.bytes_limit:
                    break
            if len(received) >= self.bytes_limit:
                log("Перевищено ліміт байтів!", msgType="error", tabs=2)
                client.send(self.generateResponse(500, "BytesLimit"))
                client.close()
                print(Fore.RED + "}" + Fore.RESET)
                continue
            d_received = received.decode()
            log("Отримано " + str(len(d_received)) + " байтів", tabs=2)
            snd = self.connected(d_received)
            log("Відправлено: " + str(len(str(snd))) + " байтів", tabs=2)
            log(str(snd), tabs=2)
            client.send(self.generateResponse(snd[0], snd[1]))
            client.close()
            log("Клієнт від'єднався!", tabs=2)
            print(Fore.RED + "}" + Fore.RESET)
            self.connections += 1
            if self.connections > 9:
                self.connections = 0

    def connected(self, msg):
        if "\r\n\r\n{" not in msg or len(msg.split("\r\n\r\n{")) != 2 or not msg.endswith("}"):
            return (500, "BadFormat")
        try:
            dic: dict = loads("{" + msg.split("\r\n\r\n{")[1])
        except Exception as ex:
            print(ex)
            return (500, "BadFormat")
        else:
            return (200, func(
                dic
            ))

    def generateResponse(self, status, content):
        return str("HTTP/1.0 " + str(status) + " " + ("OK " if status == 200 else "BAD") + self.header + str(
            len(content.encode())) + "\r\n\r\n" + str(content)).encode()


def log(message: str, msgType: str = "info", tabs: int = 0) -> None:
    print((" " * tabs) + Fore.YELLOW + "[" + Fore.BLUE + msgType.upper() + (
            " " * max(8 - len(msgType), 1)) + Fore.GREEN + datetime.now().strftime(
        "%m.%d %H:%M:%S") + Fore.YELLOW + "] " + Fore.RESET + message)


def init():
    if "VUPPY_IP" in environ:
        ip = environ["VUPPY_IP"]
    else:
        ip = DEFAULT_SERVERIP
    if "VUPPY_PORT" in environ:
        port = int(environ["VUPPY_PORT"])
    else:
        port = DEFAULT_SERVERPORT
    if "VUPPY_LMBYTES" in environ:
        bytes_limit = int(environ["VUPPY_LMBYTES"])
    else:
        bytes_limit = DEFAULT_BYTESLIMIT
    log("Запуск сервера... (" + str(ip) + ":" + str(port) + ")", msgType="system")
    Serv(port=port, bytes_limit=bytes_limit, ip=ip).start()


if __name__ == "__main__":
    init()
