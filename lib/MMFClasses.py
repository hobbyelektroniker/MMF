"""
Micropython Multitasking Framework MMF
Hardwareunabhängige Basisklassen

https://github.com/hobbyelektroniker/MMF
https://community.hobbyelektroniker.ch
https://www.youtube.com/c/HobbyelektronikerCh

Der Hobbyelektroniker, 04.04.2023
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
        self._start_time = self._millis()
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

    def step(self):
        if self._loop:
            self._loop()
        for task in self._tasks:
            task.execute()
        self._tasks = [item for item in self._tasks if not item._done]
        return not self._done 
        
    def run(self, start=None, loop=None, message=None, autoloop=True):
        self._done = False
        self._message = message
        self._loop = loop
        if start:
            start()
        if autoloop:
            while not self._done:
                self.step()

    def stop(self):
        for task in self._tasks:
            task.stop()
        self._done = True

    def notify(self, sender, topic, data):
        if self._message:
            self._message(sender, topic, data)

    def clear(self):
        self._tasks.clear()

    def add_function(self, interval, func, *args, **kwargs):
        task = FunctionTask(interval, func, *args, **kwargs)
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

    def millis(self):
        return self._millis() - self._start_time

    @classmethod
    def _millis(cls):
        return 0

    @classmethod
    def func_name(cls, func):
        return ""


class Task:
    def __init__(self, interval, immediately=False):
        self._interval = interval
        self.active = False
        self._immediately = immediately
        self._last_run = 0
        self._next_run = 0
        self._done = False
        self._step = None
        self.app = None
        
    def activate(self, app):
        self.app = app
        self._last_run = app.millis()
        self._next_run = self._last_run if self._immediately else self._last_run + self._interval
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
        self._next_run = self._last_run + self._interval
        self.step()

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, value):
        self._interval = value
        self._next_run = self._last_run + self._interval


class FunctionTask(Task):
    def __init__(self, interval, func, *args, **kwargs):
        super().__init__(interval)
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def step(self):
        self.func(*self.args, **self.kwargs)


class AfterTask(FunctionTask):
    def step(self):
        self.func(*self.args, **self.kwargs)
        self.stop()
