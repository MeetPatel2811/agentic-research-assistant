# This module defines a very simple logger utility
# used across the system to print timestamped, labeled messages.

import datetime


def log_info(message: str) -> None:
    # This function logs informational messages with a timestamp.
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[INFO  {timestamp}] {message}")


def log_error(message: str) -> None:
    # This function logs error messages with a timestamp.
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[ERROR {timestamp}] {message}")
