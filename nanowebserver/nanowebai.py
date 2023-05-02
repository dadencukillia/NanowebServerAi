# -*- coding: utf-8 -*-

import socket, base64, io, re
import numpy as np
from datetime import datetime
from os import environ  # VUPPY_IP, VUPPY_PORT, VUPPY_LMBYTES
from colorama import Fore
from colorama import init as cinit
from PIL import Image
from json import loads

cinit()

DEFAULT_BYTESLIMIT = 56000000  # bytes
DEFAULT_SERVERIP = "127.0.0.1"
DEFAULT_SERVERPORT = 8787


def imfile2nparray(Base64image: bytes):
    """
    Examples:

    >>> imfile2nparray(WholeBase64image)
    {
        "ok":True,
        "nparray":[...],
        "error":None
    }

    >>> imfile2nparray(DamagedBase64image)
    {
        "ok":False,
        "nparray":None,
        "error": ...
    }
    """
    try:
        output = np.array(
            Image.open(
                io.BytesIO(base64.b64decode(Base64image))
            )
        )
        return {
            "ok": True,
            "nparray": output,
            "error": None
        }
    except Exception as ex:
        return {
            "ok": False,
            "nparray": None,
            "error": ex
        }


class Checker:
    """
    args:
    value: any, max_length: int, min_length: int, check_digit: bool, check_round: bool, check_alpha: bool, regex: str, check_has: list, check_not_has: list, check_exists: bool, check_picture: bool

    Examples:

    >>> if Checker("string").setMaxLength(20).setMinLength(2): print("Hello!")
    Hello

    >>> if Checker("string").setMaxLength(5).setMinLength(2): print("Hello!")

    >>> if Checker("string").setMaxLength(20).setMinLength(7): print("Hello!")

    >>> print(Checker("string").setMaxLength(20).check())
    True
    """
    __value = ""
    __max_length = None
    __min_length = None
    __check_digit = False
    __check_round = False
    __check_alpha = False
    __regex = None
    __check_has = []
    __check_not_has = []
    __check_exists = False
    __check_picture = False

    def __init__(self, value: any, max_length: int = None, min_length: int = None, check_digit: bool = False,
                 check_round: bool = False, check_alpha: bool = False, regex: str = None, check_has: list = [],
                 check_not_has: list = [], check_exists: bool = False, check_picture: bool = False):
        self.__value = value
        self.__max_length = max_length
        self.__min_length = min_length
        self.__check_digit = check_digit
        self.__check_round = check_round
        self.__check_alpha = check_alpha
        self.__regex = regex
        self.__check_has = list(check_has)
        self.__check_not_has = list(check_not_has)
        self.__check_exists = check_exists
        self.__check_picture = check_picture

    def __str__(self) -> str:
        return "<check:" + str(self.__bool__()) + " " + str(self.__value) + ">"

    def __bool__(self) -> bool:
        if self.__max_length is not None and (
                type(self.__max_length) != int or len(str(self.__value)) > self.__max_length):
            return False
        if self.__min_length is not None and (
                type(self.__min_length) != int or len(str(self.__value)) < self.__min_length):
            return False
        if self.__check_digit and not str(self.__value).isdigit():
            return False
        if self.__check_round:
            try:
                if float(self.__value) != int(self.__value):
                    return False
            except:
                return False
        if self.__check_alpha and not str(self.__value).isalpha():
            return False
        if self.__regex:
            try:
                if not re.fullmatch(re.compile(self.__regex), str(self.__value)):
                    return False
            except:
                return False
        if self.__check_has and (not (type(self.__check_has) == list or type(self.__check_has) == tuple) or False in
                                 [bool(i in self.__value) for i in self.__check_has]):
            return False
        if self.__check_not_has and (not (type(self.__check_not_has) == list or type(self.__check_not_has) == tuple) or True in
                                    [bool(i in self.__value) for i in self.__check_not_has]):
            return False
        if self.__check_exists and not self.__value:
            return False
        if self.__check_picture and imfile2nparray(self.__value)["ok"] == False:
            return False
        return True

    def toBool(self) -> bool:
        """
        Same as .check() method!
        """
        return self.__bool__()

    def check(self) -> bool:
        """
        Same as .toBool() method!
        """
        return self.__bool__()

    def getValue(self) -> any:
        """
        Example:

        >>> print(Checker("just text").getValue())
        just text
        """
        return self.__value

    def getMaxLength(self) -> int:
        """
        Example:

        >>> print(Checker("just text", max_length=20).getMaxLength())
        20
        """
        return self.__max_length

    def getMinLength(self) -> int:
        """
        Example:

        >>> print(Checker("just text", min_length=10).getMinLength())
        10
        """
        return self.__min_length

    def setValue(self, value: any) -> None:
        """
        Example:

        >>> print(Checker("small", min_length=6).toBool())
        False

        >>> print(Checker("small", min_length=6).setValue("just text").toBool())
        True

        >>> print(Checker("old text").getValue())
        old text

        >>> print(Checker("old text").setValue("new text").getValue())
        new text
        """
        self.__value = value
        return self

    def setMaxLength(self, value: int) -> None:
        """
        Example:

        >>> print(Checker("just text", max_length=20).getMaxLength())
        20

        >>> print(Checker("just text", max_length=20).setMaxLength(30).getMaxLength())
        30

        >>> print(Checker("just text", max_length=2).toBool())
        False

        >>> print(Checker("just text", max_length=2).setMaxLength(20).toBool())
        True

        >>> print(Checker("just text").toBool())
        True

        >>> print(Checker("just text").setMaxLength(2).toBool())
        False
        """
        self.__max_length = value
        return self

    def setMinLength(self, value: int) -> None:
        """
        Example:

        >>> print(Checker("just text", min_length=20).getMinLength())
        20

        >>> print(Checker("just text", min_length=20).setMinLength(30).getMinLength())
        30

        >>> print(Checker("just text", min_length=2).toBool())
        True

        >>> print(Checker("just text", min_length=2).setMinLength(20).toBool())
        False

        >>> print(Checker("just text").toBool())
        True

        >>> print(Checker("just text").setMinLength(20).toBool())
        False
        """
        self.__min_length = value
        return self

    def setCheckDigit(self, value: bool) -> None:
        """
        Example:

        >>> print(Checker("it is not number").toBool())
        True

        >>> print(Checker("it is not number").setCheckDigit(True).toBool())
        False

        >>> print(Checker("20").setCheckDigit(True).toBool())
        True
        """
        self.__check_digit = value
        return self

    def setCheckRound(self, value: bool) -> None:
        """
        Example:

        >>> print(Checker(2.5).toBool())
        True

        >>> print(Checker(2.5).setCheckRound(True).toBool())
        False

        >>> print(Checker(2).setCheckRound(True).toBool())
        True

        >>> print(Checker(2.0).setCheckRound(True).toBool())
        True
        """
        self.__check_round = value
        return self

    def setCheckAlpha(self, value: bool) -> None:
        self.__check_alpha = value
        return self

    def offRegex(self) -> None:
        self.__regex = None
        return self

    def setRegex(self, regex: str) -> None:
        self.__regex = regex
        return self

    def setCheckHas(self, *args) -> None:
        """
        Example:

        >>> print(Checker("Hello, world!").toBool())
        True

        >>> print(Checker("Hello, world!").setCheckHas("e", "o", "l").toBool())
        True

        >>> print(Checker("Hello, world!").setCheckHas("e", "o", "l", "h").toBool())
        False
        """
        self.__check_has = list(args)
        return self

    def setCheckNotHas(self, *args) -> None:
        """
        Example:

        >>> print(Checker("Hello, world!").toBool())
        True

        >>> print(Checker("Hello, world!").setCheckHas("e", "o", "l").toBool())
        False

        >>> print(Checker("Hello, world!").setCheckHas("e", "o", "l", "h").toBool())
        False

        >>> print(Checker("Hello, world!").setCheckHas("p", "O", "D", "h").toBool())
        True
        """
        self.__check_not_has = list(args)
        return self

    def checkExists(self, value: bool) -> None:
        """
        >>> print(Checker(None).toBool())
        True

        >>> print(Checker("DD").toBool())
        True

        >>> print(Checker(None).checkExists(True))
        False

        >>> print(Checker("DD").checkExists(True))
        True
        """
        self.__check_exists = value
        return self

    def checkPicture(self, value: bool) -> None:
        self.__check_picture = value
        return self


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
        log("Очікуємо підключення...", msgType="SYSTEM")
        while 1:
            client, addr = self.soc.accept()
            print("Connection №" + str(self.connections) + Fore.RED + " {" + Fore.RESET)
            log("Підключено: " + addr[0], tabs=2)
            received = b''
            while 1:
                bytes = 65495
                data = client.recv(bytes)
                received += data
                if len(data) < bytes or (data.endswith(b"}") and b"\r\n\r\n{" in received):
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
        port = environ["VUPPY_PORT"]
    else:
        port = DEFAULT_SERVERPORT
    if "VUPPY_LMBYTES" in environ:
        bytes_limit = environ["VUPPY_LMBYTES"]
    else:
        bytes_limit = DEFAULT_BYTESLIMIT
    log("Запуск сервера... (" + str(ip) + ":" + str(port) + ")", msgType="SYSTEM")
    Serv(port=port, bytes_limit=bytes_limit, ip=ip).start()


if __name__ == "__main__":
    init()
