# coding=utf-8
from __future__ import absolute_import, print_function

import os

from suanpan import error, utils
from suanpan.log import logger
from suanpan.objects import HasName
from suanpan.utils import env, json

DEFAULT_MAX_VALUE_LENGTH = 120


class Arg(HasName):
    MAX_VALUE_LENGTH = DEFAULT_MAX_VALUE_LENGTH

    def __init__(self, key, **kwargs):
        self.alias = kwargs.pop("alias", None)
        self.key = key
        self.required = kwargs.pop("required", False)
        self.default = kwargs.pop("default", None)
        self.type = kwargs.pop("type", str)
        self.value = None

        self.kwargs = self.cleanParams(kwargs)
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def isSet(self):
        return self.required or self.default != self.value

    def load(self, args):
        self.value = args.get(self.key)
        if self.value is None:
            self.value = env.get(self.envKeyFormat(self.key))
        if self.required and self.value is None and self.default is None:
            raise error.ArgumentRequiredError(f"{self.key} is required")
        return self

    def format(self):
        if self.value is None:
            self.value = self.default
        else:
            try:
                self.value = self.transform(self.value)
            except Exception:
                raise error.ArgumentTypeError(
                    f"({self.name}) {self.key}: {utils.shorten(self.value, maxlen=self.MAX_VALUE_LENGTH)}"
                )
        self.logLoaded(self.value)
        return self

    def transform(self, value):
        return self.type(value)

    def clean(self):  # pylint: disable=unused-argument
        return self

    def save(self, result):  # pylint: disable=unused-argument
        self.logSaved(result.value)
        return result.value

    def cleanParams(self, params):
        return {k: v for k, v in params.items() if not k.startswith("_")}

    @property
    def keyString(self):
        return self.alias or self.key

    def logLoaded(self, value):
        logger.info(
            f"({self.name}) {self.keyString} loaded: {utils.shorten(value, maxlen=self.MAX_VALUE_LENGTH)}"
        )

    def logSaved(self, value):
        logger.info(
            f"({self.name}) {self.keyString} saved: {utils.shorten(value, maxlen=self.MAX_VALUE_LENGTH)}"
        )

    def fixGlobalKey(self, key):
        return key.replace("-", "_")

    def envKeyFormat(self, key):
        return f"SP_{self.fixGlobalKey(key).upper()}"

    def getOutputTmpValue(self, *args):
        pass

    def getOutputTmpArg(self, *args):
        value = self.getOutputTmpValue(  # pylint: disable=assignment-from-no-return
            *args
        )
        return (f"--{self.key}", value) if value is not None else tuple()


class String(Arg):
    pass

class Int(Arg):
    @classmethod
    def transform(cls, value):
        return int(value)

class Float(Arg):
    @classmethod
    def transform(cls, value):
        return float(value)


class Bool(Arg):
    def __init__(self, key, **kwargs):
        kwargs.setdefault("default", False)
        super(Bool, self).__init__(key, **kwargs)

    @classmethod
    def transform(cls, value):
        if value.lower() in ("yes", "true", "t", "y"):
            return True
        if value.lower() in ("no", "false", "f", "n"):
            return False
        raise error.ArgumentError(cls.__name__)


class List(Arg):
    def transform(self, value):
        return [i.strip() for i in value.split(",") if i.strip()]


class ListOfString(List):
    pass


class ListOfInt(List):
    def transform(self, value):
        items = super(ListOfInt, self).transform(value)
        return [Int.transform(i) for i in items]


class ListOfFloat(List):
    def transform(self, value):
        items = super(ListOfFloat, self).transform(value)
        return [Float.transform(i) for i in items]


class ListOfBool(List):
    def transform(self, value):
        items = super(ListOfBool, self).transform(value)
        return [Bool.transform(i) for i in items]


class Json(String):
    def transform(self, value):
        if value is not None:
            value = json.loads(value)
        return value

    def save(self, result):
        super(Json, self).save(result)
        return json.dumps(result.value)


class IntOrFloat(Arg):
    @classmethod
    def transform(cls, value):
        return Float.transform(value) if "." in value else Int.transform(value)


class IntFloatOrString(Arg):
    def transform(self, value):
        try:
            Float.transform(value)
            return IntOrFloat.transform(value)
        except ValueError:
            return value
        except TypeError:
            return value


class BoolOrString(Arg):
    def transform(self, value):
        return value if value == "auto" else Bool.transform(value)


class BoolOrInt(Arg):
    def transform(self, value):
        try:
            return Bool.transform(value)
        except error.ArgumentError:
            return Int.transform(value)


class StringOrListOfFloat(ListOfFloat):
    def transform(self, value):
        if "," in value:
            return super(StringOrListOfFloat, self).transform(value)
        return value
