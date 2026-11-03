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
core.CGSessionCopyCurrentDictionary.restype = ctypes.c_void_p
core.CGSessionCopyCurrentDictionary.argtypes = []
core.CFStringCreateWithCString.restype = ctypes.c_void_p
core.CFStringCreateWithCString.argtypes = [
    ctypes.c_void_p,
    ctypes.c_char_p,
    ctypes.c_uint32,
]
core.CFDictionaryGetValue.restype = ctypes.c_void_p
core.CFDictionaryGetValue.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
core.CFBooleanGetValue.restype = ctypes.c_bool
core.CFBooleanGetValue.argtypes = [ctypes.c_void_p]
core.CFRelease.restype = None
core.CFRelease.argtypes = [ctypes.c_void_p]

# Absent while the session is open. True after lock, including lid close.
LOCKED_KEY = core.CFStringCreateWithCString(
    None, b"CGSSessionScreenIsLocked", 0x08000100
)


def point():
    event = core.CGEventCreate(None)
    if not event:
        return None
    location = core.CGEventGetLocation(event)
    core.CFRelease(event)
    return location.x, location.y


def locked():
    session = core.CGSessionCopyCurrentDictionary()
    if not session:
        return False
    value = core.CFDictionaryGetValue(session, LOCKED_KEY)
    is_locked = bool(value and core.CFBooleanGetValue(value))
    core.CFRelease(session)
    return is_locked


def stop():
    # q never reaches this function, and neither does lock. A pointer exit
    # is someone who did not dismiss the screen on purpose, so record them
    # for two minutes. Wait until the camera is open; it leaves this session
    # and keeps recording after the window is gone.
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
    # Lock ends the watch without recording. Wake-from-lock moves the
    # pointer, and that is the owner, not an unattended session.
    if locked():
        raise SystemExit(0)
    current = point()
    if current is None:
        continue
    if abs(current[0] - origin[0]) >= MOVE or abs(current[1] - origin[1]) >= MOVE:
        if locked():
            raise SystemExit(0)
        stop()
        raise SystemExit(0)
