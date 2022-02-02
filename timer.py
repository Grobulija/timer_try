import functools
from dataclasses import dataclass, field
import time
from datetime import timedelta
from typing import Callable, ClassVar, Dict, Optional
from string import Formatter


class TimerError(Exception):
    """Custom exception for Timer class"""


@dataclass
class Timer:
    timers: ClassVar[Dict[str, str]] = dict()
    name: Optional[str] = None
    text: str = ""
    logger: Optional[Callable[[str], None]] = None
    _start_time: Optional[str] = field(default=None, init=False, repr=False)
    format: str = ""
    run_count: int = 0
    index: int = 0
    order: list = None

    def __post_init__(self) -> None:
        if self.name is None:
            self.name = "block_" + str(self.__class__.index)
        self.__class__.index += 1
        self.timers.setdefault(self.name, "")
        self.text = self.__class__.run_count * '\t' + "block \"" + self.name + "\": {}"

    def start(self) -> None:
        self.__class__.run_count += 1
        if self._start_time is not None:
            raise TimerError(f"Timer is running")

        self._start_time = str(time.perf_counter())

    def stop(self) -> str:
        self.__class__.run_count -= 1
        if self._start_time is None:
            raise TimerError(f"Timer is not running")

        elapsed_time = time.perf_counter() - float(self._start_time)
        self._start_time = None

        elapsed_time = timedelta(seconds=elapsed_time)
        if self.format:
            elapsed_time = self.str_f_delta(elapsed_time, self.format)
        else:
            elapsed_time = self.str_f_delta(elapsed_time)

        if self.logger:
            self.logger(self.text.format(elapsed_time))
        if self.name:
            self.timers[self.name] += str(elapsed_time)
        if not self.__class__.order:
            self.__class__.order = []
        self.__class__.order.insert(0, self.text.format(elapsed_time))
        return str(elapsed_time)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *exc_info):
        self.stop()

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper_timer(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return wrapper_timer

    @classmethod
    def get_count(cls):
        return cls.run_count

    @classmethod
    def get_order(cls):
        for line in cls.order:
            print(line)

    @staticmethod
    def str_f_delta(time_delta, fmt='{MS:4}ms'):
        time_delta *= 1000
        remainder = int(time_delta.total_seconds())
        f = Formatter()
        desired_fields = [field_tuple[1] for field_tuple in f.parse(fmt)]
        possible_fields = ('D', 'H', 'M', 'S', 'MS')
        constants = {'D': 86400000, 'H': 3600000, 'M': 60000, 'S': 1000, 'MS': 1}
        values = {}
        for field in possible_fields:
            if field in desired_fields and field in constants:
                values[field], remainder = divmod(remainder, constants[field])
        return f.format(fmt, **values)
