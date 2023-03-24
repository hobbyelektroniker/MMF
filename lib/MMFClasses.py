"""
Micropython Multitasking Framework MMF
Hardwareunabhängige Basisklassen

https://github.com/hobbyelektroniker/MMF
https://community.hobbyelektroniker.ch
https://www.youtube.com/c/HobbyelektronikerCh

Der Hobbyelektroniker, 24.03.2023
MIT License gemäss Angaben auf Github
"""

class _Application:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            return cls._instance
        else:
            raise ValueError("Only one instance allowed")

    def __init__(self):
        self._tasks = []
        self._done = False
        self._loop = None
        self._message = None
        self.settings = {}
        self.load_settings()

    @classmethod
    def app(cls):
        return cls._instance

    def load_settings(self):
        try:
            with open("settings.txt", 'r') as f:
                self.settings = eval(f.read())
        except:
            self.settings = {}

    def save_settings(self):
        with open("settings.txt", 'w') as f:
            f.write(str(self.settings))

    def run(self, start=None, loop=None, message=None, channel=0):
        self._done = False
        self._channel = channel
        self._message = message
        if start:
            start()
        while not self._done:
            if loop:
                loop()
            for task in self._tasks:
                task.execute()
            self._tasks = [item for item in self._tasks if not item._done]

    def stop(self):
        self._done = True

    def notify(self, sender, topic, data):
        if self._message:
            self._message(sender, topic, data)

    def clear(self):
        self._tasks.clear()

    def add_function(self, time, func, *args, **kwargs):
        task = FunctionTask(time, func, *args, **kwargs)
        self._tasks.append(task)
        task.activate(self)
        return task

    def add_components(self, *args):
        for task in args:
            self._tasks.append(task)
            task.activate(self)

    def after(self, time, func, *args, **kwargs):
        task = AfterTask(time, func, *args, **kwargs)
        self.add_components(task)
        return task


    @classmethod
    def millis(cls):
        return 0

    @classmethod
    def func_name(cls, func):
        return ""


class Task:
    def __init__(self, time, immediately=False):
        self._time = time
        self.active = False
        self._immediately = immediately
        self._last_run = 0
        self._next_run = 0
        self._done = False
        self._step = None
        self.app = None
        
    def activate(self, app):
        self.app = app
        self._last_run = 0 if self._immediately else app.millis()
        self._next_run = self._last_run + self._time
        self.active = True

    def step(self):
        pass

    def stop(self):
        self._done = True

    def execute(self):
        if self._done or not self.active:
            return
        time_stamp = self.app.millis()
        if time_stamp < self._next_run:
            return
        self._last_run = time_stamp
        self._next_run = self._last_run + self._time
        self.step()

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value
        self._next_run = self._last_run + self._time


class FunctionTask(Task):
    def __init__(self, time, func, *args, **kwargs):
        super().__init__(time)
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def step(self):
        self.func(*self.args, **self.kwargs)


class AfterTask(FunctionTask):
    def step(self):
        self.func(*self.args, **self.kwargs)
        self.stop()
