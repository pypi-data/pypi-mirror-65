# coding=utf-8
from __future__ import absolute_import, print_function

import contextlib
import copy
import itertools
import time
import traceback
import uuid

from suanpan import asyncio, error, g, runtime, utils
from suanpan.arguments import Bool, BoolOrInt, Float, Int, String
from suanpan.components import Arguments, Component
from suanpan.dw import dw
from suanpan.interfaces import (
    HasCallHooks,
    HasDevMode,
    HasExitHooks,
    HasInitHooks,
    HasLogger,
    HasTriggerHooks,
)
from suanpan.interfaces.optional import HasBaseServices
from suanpan.log import logger
from suanpan.mq import mq
from suanpan.mstorage import mstorage
from suanpan.objects import Context
from suanpan.storage import storage
from suanpan.utils import json


class Handler(Component):
    def run(self, steamObj, message, *arg, **kwargs):
        self.callBeforeInitHooks()
        context = self.init(steamObj, message)
        self.callAfterInitHooks(context)

        self.callBeforeCallHooks(context)
        if not self.runFunc:
            raise error.ComponentHandlerNotSet()
        if not callable(self.runFunc):
            raise error.ComponentHandlerNotCallable(self.name)
        results = self.runFunc(steamObj, context, *arg, **kwargs)
        self.callAfterCallHooks(context)

        self.callBeforeSaveHooks(context)
        outputs = self.save(results, message=message)
        self.callAfterSaveHooks(context)

        self.callBeforeCleanHooks(context)
        self.clean()
        self.callAfterCleanHooks()

        return outputs

    def beforeInit(self):
        logger.debug(f"Handler {self.name} starting...")

    def init(self, steamObj, message):
        self.argsDict = self.getArgsDict(message)
        context = self._getContext(message)
        args = self.loadComponentArguments(self.argsDict)
        args.update(steamObj.args)
        context.update(args=args)
        return context

    def load(self, args, argsDict=None):
        logger.info("Loading Arguments:")
        argsDict = argsDict or self.argsDict
        argsDict = {
            f"{arg.key}": argsDict.get(f"in{i+1}")
            for i, arg in enumerate(args)
            if argsDict.get(f"in{i+1}") is not None
        }
        args = self.loadFormatArguments(args, argsDict)
        return Arguments.froms(*args)

    def loadComponentArguments(self, argsDict=None):
        logger.info("Loading Component Arguments:")
        argsDict = argsDict or self.argsDict
        arguments = copy.deepcopy(self.getArguments(exclude="outputs"))
        argsDict = {
            f"{arg.key}": argsDict.get(f"in{i+1}")
            for i, arg in enumerate(arguments)
            if argsDict.get(f"in{i+1}") is not None
        }
        argsDict = argsDict or self.argsDict
        args = self.loadFormatArguments(arguments, argsDict)
        return Arguments.froms(*args)

    def getArgsDict(self, message):
        return message or {}

    @contextlib.contextmanager
    def context(self, message):
        yield Context.froms(message=message)

    def save(self, results, args=None, message=None):
        args = args or copy.deepcopy(self.getArguments(include="outputs"))
        shortRequestID = self.shortenRequestID(message["id"])
        outputArgsDict = {
            arg.key: arg.getOutputTmpValue(
                "studio", g.userId, g.appId, shortRequestID, g.nodeId, f"out{i+1}"
            )
            for i, arg in enumerate(args)
        }
        args = self.loadCleanArguments(args, outputArgsDict)
        return self.saveOutputs(args, results)

    def afterSave(self, context):  # pylint: disable=unused-argument
        logger.debug(f"Handler {self.name} done.")

    def saveOutputs(self, args, results):
        if results is not None:
            outputs = super(Handler, self).saveOutputs(args, results)
            outputs = self.formatAsOuts(args, outputs)
            outputs = self.stringifyOuts(outputs)
            return outputs
        return None

    def formatAsOuts(self, args, results):
        return {
            f"out{i+1}": self.getArgumentValueFromDict(results, arg)
            for i, arg in enumerate(args)
        }

    def stringifyOuts(self, outs):
        return {k: str(v) for k, v in outs.items() if v is not None}

    def shortenRequestID(self, requestID):
        return requestID.replace("-", "")


class StreamBase(HasBaseServices, HasLogger, HasDevMode, HasInitHooks, HasExitHooks):

    DEFAULT_LOGGER_MAX_LENGTH = 120
    DEFAULT_MESSAGE = {}
    DEFAULT_STREAM_CALL = "call"
    STREAM_ARGUMENTS = [
        String("stream-recv-queue", default=f"mq-{g.nodeId}"),
        BoolOrInt("stream-recv-queue-block", default=60000),
        Float("stream-recv-queue-delay", default=0),
        Int("stream-recv-queue-max-length", default=1000),
        Bool("stream-recv-queue-trim-immediately", default=False),
        Bool("stream-recv-queue-retry", default=False),
        Int("stream-recv-queue-retry-max-count", default=100),
        Float("stream-recv-queue-retry-timeout", default=1.0),
        Int("stream-recv-queue-retry-max-times", default=3),
        String("stream-send-queue", default="mq-master"),
        Int("stream-send-queue-max-length", default=1000),
        Bool("stream-send-queue-trim-immediately", default=False),
    ]

    def __init__(self):
        super(StreamBase, self).__init__()
        self.argsDict = {}
        self.args = None
        self.options = {}

    def beforeInit(self):
        logger.logDebugInfo()
        logger.debug(f"Stream {self.name} starting...")

    def init(self, *args, **kwargs):
        self.argsDict = self.getArgsDict(*args, **kwargs)
        self.args = self.loadGlobalArguments(self.argsDict)
        self.options = self.getOptions(self.args)
        self.setBaseServices(self.args)
        self.args.update(self.loadComponentArguments(self.argsDict))
        return Context.froms(args=self.args)

    def loadGlobalArguments(self, argsDict=None):
        logger.info("Loading Global Arguments:")
        argsDict = argsDict or self.argsDict
        args = self.loadFormatArguments(self.getGlobalArguments(), argsDict)
        return Arguments.froms(*args)

    def loadComponentArguments(self, argsDict=None):
        logger.info("Loading Components Arguments:")
        argsDict = argsDict or self.argsDict
        args = self.loadFormatArguments(self.getComponentArguments(), argsDict)
        return Arguments.froms(*args)

    def getGlobalArguments(self, *args, **kwargs):
        arguments = super(StreamBase, self).getGlobalArguments(*args, **kwargs)
        return arguments + self.STREAM_ARGUMENTS

    def generateRequestId(self):
        return uuid.uuid4().hex

    def generateMessage(self, **kwargs):
        message = {}
        message.update(self.DEFAULT_MESSAGE, **kwargs)
        message.setdefault("type", self.DEFAULT_STREAM_CALL)
        message["id"] = self.generateRequestId()
        return message

    def formatMessage(self, message, msg, costTime=None):
        msgs = [message["id"], message.get("type", self.DEFAULT_STREAM_CALL), msg]
        if costTime is not None:
            msgs.insert(-1, f"{costTime}s")
        return " - ".join(msgs)

    def streamCall(self, message, *args, **kwargs):
        logger.info(self.formatMessage(message, msg="Start"))
        startTime = time.time()
        try:
            handler = self.getHandler(message)
            outputs = handler.run(self, message, *args, **kwargs) or {}
            endTime = time.time()
            costTime = round(endTime - startTime, 3)
            logger.info(self.formatMessage(message, msg="Done", costTime=costTime))
            if outputs:
                self.sendSuccessMessage(message, outputs)
        except Exception:  # pylint: disable=broad-except
            tracebackInfo = traceback.format_exc()
            endTime = time.time()
            costTime = round(endTime - startTime, 3)
            logger.error(
                self.formatMessage(message, msg=tracebackInfo, costTime=costTime)
            )
            self.sendFailureMessage(message, tracebackInfo)

    def handlerCallback(self, *args, **kwargs):
        return self.streamCall(self.generateMessage(), *args, **kwargs)

    def getHandler(self, message):
        streamCall = message.get("type", self.DEFAULT_STREAM_CALL)
        handler = getattr(self, streamCall, None)
        if not handler or not isinstance(handler, Handler):
            raise error.StreamError(f"Unknown stream handler {self.name}.{streamCall}")
        return handler

    @runtime.globalrun
    def start(self, *args, **kwargs):
        self.callBeforeInitHooks()
        context = self.init(*args, **kwargs)
        self.callAfterInitHooks(context)
        self.registerBeforeExitHooks(context)
        self.run()

    def run(self):
        self.startCallLoop()

    def startCallLoop(self):
        if self.options["recvQueueRetry"]:
            self.retryPendingMessages()
        for message in self.subscribe():
            self.handleMessage(message.get("data", {}))

    @runtime.saferun
    def handleMessage(self, message):
        self.streamCall(message)

    def setDefaultMessageType(self, message):
        message["data"].setdefault("type", self.DEFAULT_STREAM_CALL)
        return message

    def getMessageExtraData(self, message):
        extra = message["data"].get("extra")
        extra = json.loads(extra) if extra else {}
        message["data"].update(extra=extra)
        return message

    def getOptions(self, args):
        return self.defaultArgumentsFormat(args, self.STREAM_ARGUMENTS)

    def subscribe(self, **kwargs):
        for message in mq.subscribeQueue(
            self.options["recvQueue"],
            group=g.nodeGroup,
            consumer=g.nodeId,
            block=self.options["recvQueueBlock"],
            delay=self.options["recvQueueDelay"],
            **kwargs,
        ):
            message = self.setDefaultMessageType(message)
            message = self.getMessageExtraData(message)
            yield message

    def recv(self, **kwargs):
        return mq.recvMessages(
            self.options["recvQueue"], group=g.nodeId, consumer=self.name, **kwargs,
        )

    def _send(self, message, data, queue=None, extra=None):
        queue = queue or self.options["sendQueue"]
        message.setdefault("extra", {})
        message["extra"].update(extra or {})
        data = {
            "node_id": g.nodeId,
            "request_id": message["id"],
            "type": self.DEFAULT_STREAM_CALL,
            "extra": json.dumps(message["extra"]),
            **data,
        }
        logger.debug(
            utils.shorten(f"Send to `{queue}`: {data}", self.DEFAULT_LOGGER_MAX_LENGTH)
        )
        return mq.sendMessage(
            queue,
            data,
            maxlen=self.options["sendQueueMaxLength"],
            trimImmediately=self.options["sendQueueTrimImmediately"],
        )

    def sendSuccessMessage(self, message, data, queue=None, extra=None):
        if not all(key.startswith("out") for key in data):
            raise error.StreamError(
                "Success Message data only accept keys starts with 'out'"
            )
        data = {key: value for key, value in data.items() if value is not None}
        data.update(success="true")
        return self._send(message, data, queue=queue, extra=extra)

    def sendFailureMessage(self, message, msg, queue=None, extra=None):
        if not isinstance(msg, str):
            raise error.StreamError("Failure Message msg only accept string")
        data = {"msg": msg, "success": "false"}
        return self._send(message, data, queue=queue, extra=extra)

    def send(self, results, queue=None, message=None, args=None, extra=None, **_):
        message = message or self.generateMessage()
        outputs = self.getHandler(message).save(results, args=args, message=message)
        return self.sendSuccessMessage(message, outputs, queue=queue, extra=extra)

    def sendError(self, msg, queue=None, message=None, extra=None):
        message = message or self.generateMessage()
        return self.sendFailureMessage(message, msg, queue=queue, extra=extra)

    def sendMissionMessage(self, message, data, queue=None, extra=None):
        if not all(key.startswith("in") for key in data):
            raise error.StreamError(
                "Mission Message data only accept keys starts with 'in'"
            )
        data = {key: value for key, value in data.items() if value is not None}
        data.update(id=message["id"])
        return self._send(message, data, queue=queue, extra=extra)

    def retryPendingMessages(self, **kwargs):
        return mq.retryPendingMessages(
            self.options["recvQueue"],
            group=g.nodeGroup,
            consumer=g.nodeId,
            count=self.options["recvQueueRetryMaxCount"],
            maxTimes=self.options["recvQueueRetryMaxTimes"],
            timeout=self.options["recvQueueRetryTimeout"],
            maxlen=self.options["recvQueueMaxLength"],
            trimImmediately=self.options["recvQueueTrimImmediately"],
            **kwargs,
        )

    def keysAllIn(self, keys, kset):
        return len(set(keys) - set(kset)) == 0


class Stream(StreamBase):
    INTERVAL = 0
    TRIGGER_ARGUMENTS = [Float("triggerInterval", default=0)]
    DEFAULT_TRIGGER_CALL = "trigger"

    def getGlobalArguments(self, *args, **kwargs):
        arguments = super(Stream, self).getGlobalArguments(*args, **kwargs)
        return arguments + self.TRIGGER_ARGUMENTS

    def _list(self, data):
        if isinstance(data, (tuple, list)):
            return data
        if data is None:
            return []
        return [data]

    @property
    def interval(self):
        _interval = getattr(self, "_interval", None)
        if _interval is not None:
            return _interval
        return self.args.triggerInterval or self.INTERVAL

    @interval.setter
    def interval(self, value):
        if not isinstance(value, (int, float)):
            raise error.StreamError("Interval must be int or float")
        setattr(self, "_interval", value)

    def loop(self):
        while True:
            yield
            time.sleep(self.interval)

    def triggerCall(self, *args, **kwarags):
        return self.streamCall(
            self.generateMessage(type=self.DEFAULT_TRIGGER_CALL), *args, **kwarags
        )

    def startTriggerLoop(self):
        for data in self.loop():
            self.triggerCall(*self._list(data))

    def getInitialRunners(self):
        runners = []
        stream = getattr(self, self.DEFAULT_STREAM_CALL, None)
        if stream and stream.runFunc:
            runners.append(self.startCallLoop)
        trigger = getattr(self, self.DEFAULT_TRIGGER_CALL, None)
        if trigger and trigger.runFunc:
            runners.append(self.startTriggerLoop)
        return runners

    def startOnlyRunner(self, runners):
        runners[0]()

    def startMultiRunners(self, runners):
        asyncio.wait(asyncio.run(runners, workers=len(runners), thread=True))

    def run(self):
        runners = self.getInitialRunners()
        if not runners:
            raise error.StreamError("Stream can not start: No Method implemented!")

        if len(runners) == 1:
            self.startOnlyRunner(runners)
        else:
            self.startMultiRunners(runners)

    def triggerSend(self, results, queue=None, message=None, args=None, extra=None):
        message = message or self.generateMessage(type=self.DEFAULT_TRIGGER_CALL)
        return self.send(results, queue=queue, message=message, args=args, extra=extra)
