# coding=utf-8
from __future__ import absolute_import, print_function

from suanpan import error
from suanpan.app.base import BaseApp
from suanpan.model.arguments import HotReloadModel
from suanpan.stream import Handler, Stream
from suanpan.utils import functional

COMPONENT_ARGUMENT_CLASSES = (HotReloadModel,)


class TriggerApp(BaseApp):
    def __init__(self, stream, *args, **kwargs):
        super(TriggerApp, self).__init__(*args, **kwargs)
        self.stream = stream
        self.stream.trigger = Handler()

    def __call__(self, funcOrApp):
        if not isinstance(funcOrApp, BaseApp):
            self.stream.trigger.use(functional.instancemethod(funcOrApp))
        return self

    def interval(self, _interval):
        self.stream.INTERVAL = _interval
        return self

    def loop(self, _loop):
        self.stream.loop = functional.instancemethod(_loop)
        return self

    def input(self, argument):
        if isinstance(argument, COMPONENT_ARGUMENT_CLASSES):
            self.stream.ARGUMENTS.append(argument)
        else:
            self.stream.trigger.input(argument)
        return self

    def output(self, argument):
        if isinstance(argument, HotReloadModel):
            raise error.AppError(f"{argument.name} can't be set as output!")
        self.stream.trigger.output(argument)
        return self

    def param(self, argument):
        self.stream.ARGUMENTS.append(argument)
        return self

    def column(self, argument):
        self.stream.ARGUMENTS.append(argument)
        return self

    def beforeInit(self, hook):
        self.stream.addBeforeInitHooks(hook)
        return hook

    def afterInit(self, hook):
        self.stream.addAfterInitHooks(hook)
        return hook

    def beforeCall(self, hook):
        self.stream.trigger.addBeforeCallHooks(hook)
        return hook

    def afterCall(self, hook):
        self.stream.trigger.addAfterCallHooks(hook)
        return hook

    def beforeExit(self, hook):
        self.stream.addBeforeExitHooks(hook)
        return hook

    def load(self, *args, **kwargs):
        return self.stream.trigger.load(*args, **kwargs)

    def send(self, *args, **kwargs):
        return self.stream.triggerSend(*args, **kwargs)


class StreamApp(BaseApp):
    def __init__(self, *args, **kwargs):
        super(StreamApp, self).__init__(*args, **kwargs)
        self.stream = Stream()
        self.stream.call = Handler()
        self._trigger = TriggerApp(self.stream)

    def __call__(self, funcOrApp):
        if not isinstance(funcOrApp, BaseApp):
            self.stream.call.use(functional.instancemethod(funcOrApp))
        return self

    def start(self, *args, **kwargs):
        return self.stream.start(*args, **kwargs)

    def input(self, argument):
        if isinstance(argument, COMPONENT_ARGUMENT_CLASSES):
            self.stream.ARGUMENTS.append(argument)
        else:
            self.stream.call.input(argument)
        return self

    def output(self, argument):
        if isinstance(argument, HotReloadModel):
            raise error.AppError(f"{argument.name} can't be set as output!")
        self.stream.call.output(argument)
        return self

    def param(self, argument):
        self.stream.ARGUMENTS.append(argument)
        return self

    def column(self, argument):
        self.stream.ARGUMENTS.append(argument)
        return self

    def beforeInit(self, hook):
        self.stream.addBeforeInitHooks(hook)
        return hook

    def afterInit(self, hook):
        self.stream.addAfterInitHooks(hook)
        return hook

    def beforeCall(self, hook):
        self.stream.call.addBeforeCallHooks(hook)
        return hook

    def afterCall(self, hook):
        self.stream.call.addAfterCallHooks(hook)
        return hook

    def beforeExit(self, hook):
        self.stream.addBeforeExitHooks(hook)
        return hook

    def load(self, *args, **kwargs):
        return self.stream.call.load(*args, **kwargs)

    def save(self, *args, **kwargs):
        return self.stream.send(*args, **kwargs)

    def send(self, *args, **kwargs):
        return self.stream.send(*args, **kwargs)

    @property
    def args(self):
        return self.stream.args

    @property
    def trigger(self):
        return self._trigger
