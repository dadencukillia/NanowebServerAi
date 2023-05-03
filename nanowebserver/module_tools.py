from __future__ import annotations
from PIL import Image
from typing import Self
import numpy as np
import base64, io, re

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

    def setValue(self, value: any) -> Self:
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

    def setMaxLength(self, value: int) -> Self:
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

    def setMinLength(self, value: int) -> Self:
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

    def setCheckDigit(self, value: bool) -> Self:
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

    def setCheckRound(self, value: bool) -> Self:
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

    def setCheckAlpha(self, value: bool) -> Self:
        self.__check_alpha = value
        return self

    def offRegex(self) -> Self:
        self.__regex = None
        return self

    def setRegex(self, regex: str) -> Self:
        self.__regex = regex
        return self

    def setCheckHas(self, *args) -> Self:
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

    def setCheckNotHas(self, *args) -> Self:
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

    def checkExists(self, value: bool) -> Self:
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

    def checkPicture(self, value: bool) -> Self:
        self.__check_picture = value
        return self