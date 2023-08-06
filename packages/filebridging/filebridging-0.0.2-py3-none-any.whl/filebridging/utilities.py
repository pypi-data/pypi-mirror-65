"""Useful functions."""
import datetime
import logging
import shutil
import signal
import sys
from typing import Union

units_of_measurements = {
    1: 'bytes',
    1000: 'KB',
    1000 * 1000: 'MB',
    1000 * 1000 * 1000: 'GB',
    1000 * 1000 * 1000 * 1000: 'TB',
}


def get_file_size_representation(file_size):
    scale, unit = get_scale_and_unit(file_size=file_size)
    if scale < 10:
        return f"{file_size} {unit}"
    return f"{(file_size // (scale / 100)) / 100:.2f} {unit}"


def get_scale_and_unit(file_size):
    scale, unit = min(units_of_measurements.items())
    for scale, unit in sorted(units_of_measurements.items(), reverse=True):
        if file_size > scale:
            break
    return scale, unit


def print_progress_bar(prefix='',
                       suffix='',
                       done_symbol="#",
                       pending_symbol=".",
                       progress=0,
                       scale=10):
    progress_showed = (progress // scale) * scale
    line_width, _ = shutil.get_terminal_size()
    line = (f"{prefix}"
            f"{done_symbol * (progress_showed // scale)}"
            f"{pending_symbol * ((100 - progress_showed) // scale)}\t"
            f"{progress}%"
            f"{suffix}      ")
    line = line.replace('\t', ' ' * 4)
    if line_width < 5:
        line = '.' * line_width
    elif len(line) > line_width:
        line = line[:line_width-5] + '[...]'
    sys.stdout.write(
        line + '\r'
    )
    sys.stdout.flush()


def timed_action(interval: Union[int, float, datetime.timedelta] = None):
    """Do not perform decorated action before `interval`.

    `interval` may be an int number of seconds or a datetime.timedelta object.
    Usage:
    @timed_action(1)
    def print_sum(a, b):
        print(a + b)

    for i, j in enumerate(range(1000, 10000, 10)):
        print_sum(i, j)
        time.sleep(0.1)
    """
    now = datetime.datetime.now
    last_call = now()
    if type(interval) in (int, float):
        timedelta = datetime.timedelta(seconds=interval)
    elif isinstance(interval, datetime.timedelta):
        timedelta = interval

    def timer(function_to_time):
        def timed_function(*args, **kwargs):
            nonlocal last_call
            if now() > last_call + timedelta:
                last_call = now()
                return function_to_time(*args, **kwargs)
            return
        return timed_function

    return timer


def timed_input(message: str = None,
                timeout: int = 5):
    class TimeoutExpired(Exception):
        pass

    def interrupted(signal_number, stack_frame):
        """Called when read times out."""
        raise TimeoutExpired

    if message is None:
        message = f"Enter something within {timeout} seconds"

    signal.alarm(timeout)
    signal.signal(signal.SIGALRM, interrupted)
    try:
        given_input = input(message)
    except TimeoutExpired:
        given_input = None
        print()  # Print end of line
        logging.info("Timeout!")
    signal.alarm(0)
    return given_input
