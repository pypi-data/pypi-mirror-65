"""Useful functions."""

import logging
import signal
import sys

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
    sys.stdout.write(
        f"{prefix}"
        f"{done_symbol * (progress_showed // scale)}"
        f"{pending_symbol * ((100 - progress_showed) // scale)}\t"
        f"{progress}%"
        f"{suffix}      \r"
    )
    sys.stdout.flush()


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
