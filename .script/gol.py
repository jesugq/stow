#!/usr/bin/env python3

import ctypes
import os
import signal
import subprocess
import sys
import time

# One Quartz point. The animation is started from the keyboard, so any
# real pointer travel means the machine is back in use.
MOVE = 1

drift_pid = int(sys.argv[1])
pane = sys.argv[2]

core = ctypes.CDLL("/System/Library/Frameworks/CoreGraphics.framework/CoreGraphics")


class CGPoint(ctypes.Structure):
    _fields_ = [("x", ctypes.c_double), ("y", ctypes.c_double)]


core.CGEventCreate.restype = ctypes.c_void_p
core.CGEventCreate.argtypes = [ctypes.c_void_p]
core.CGEventGetLocation.restype = CGPoint
core.CGEventGetLocation.argtypes = [ctypes.c_void_p]
core.CFRelease.restype = None
core.CFRelease.argtypes = [ctypes.c_void_p]


def point():
    event = core.CGEventCreate(None)
    if not event:
        return None
    location = core.CGEventGetLocation(event)
    core.CFRelease(event)
    return location.x, location.y


def stop():
    # q never reaches this function. A pointer exit is someone who did not
    # dismiss the screen on purpose, so record them for two minutes. Wait until
    # the camera is open; it leaves this session and keeps recording after
    # the window is gone.
    subprocess.run(
        [os.path.expanduser("~/.script/cam"), "start", "120"],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    # Close the thinking split first. The shell then exits, the afk
    # window is destroyed, and tmux selects the previous window.
    if pane:
        subprocess.run(
            ["tmux", "kill-pane", "-t", pane],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    for sig in (signal.SIGTERM, signal.SIGKILL):
        try:
            os.kill(drift_pid, sig)
        except OSError:
            return
        deadline = time.monotonic() + 0.2
        while time.monotonic() < deadline:
            try:
                os.kill(drift_pid, 0)
            except OSError:
                return
            time.sleep(0.02)


origin = None
while origin is None:
    origin = point()
    if origin is None:
        time.sleep(0.05)

while True:
    time.sleep(0.05)
    current = point()
    if current is None:
        continue
    if abs(current[0] - origin[0]) >= MOVE or abs(current[1] - origin[1]) >= MOVE:
        stop()
        raise SystemExit(0)
