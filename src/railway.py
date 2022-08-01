#!/usr/bin/python3

__author__ = "Petter J. Barhaugen (petter@petternett.no)"

import os
import time
import random
import math
from datetime import datetime, timedelta
from xlib import XEvents

# TODO (now): Bind movement to velocity

# TODO (later): try system.stdout.write() instead of print for status bar?


# DELAY = time within which before no. keystrokes resets
# DELAY = 0.1
FPS = 30
DELAY = 1.0 / FPS
MS_PER_UPDATE = DELAY

WIDTH = 16
PLAYER_POS = 3

MAX_SPEED = 1
FRICTION_CONST = 0.5 # TODO: adjust
EVTS_MULTIPLIER = 1   #       these

PLAYER_CHAR = '🚃'
RAIL_CHAR = '..'
FIRE_CHAR = '🔥'
CACTUS_CHAR = '🌵'

world = [RAIL_CHAR] * WIDTH
foreground = [RAIL_CHAR] * WIDTH
background = [None] * WIDTH

velocity = 0.0
total_km = 0.0

debug_text = None


def render():
    os.system("clear")

    # print(f"Velocity: {velocity:<5.2f} ", end="")
    print(f"Total km: {total_km:.2f} ", end="")

    # Compose world
    world = [x for x in foreground]
    # for i in range(0, WIDTH):
    #     if background[i] is not None: world[i] = background[i]
    world[PLAYER_POS] = PLAYER_CHAR
    if velocity > 50: world[PLAYER_POS-1] = FIRE_CHAR


    # Print world
    for i in range(0, WIDTH-1):
        print(world[i], end="")
    print()


    # Print debug
    if debug_text: print(f"DEBUG: {debug_text}")


def debug(text):
    global debug_text
    debug_text = text


def run():
    global velocity, foregroud, background, total_km

    ax = 0.0

    events = XEvents()
    events.start()

    # Initial render
    render()


    # Actual game loop:
    # - Process input
    # - Update physics, world
    # - Render
    # - Sleep
    while True:
        cur_time = time.time()

        n_evts = 0

        # Process input. Get number of events in cur tick:
        if (evt := events.next_event()):
            n_evts += 1 # * EVTS_MULTIPLIER
        elif n_evts > 0:
            n_evts -= 1


        # Add number of events to velocity. If no events, reduce velocity.
        if n_evts > 0:
            ax += 0.01
        elif velocity > 0.02:  # ugly hack. figure out why velocity goes below 0 sometimes
            ax -= 0.01
        elif velocity <= 0:
            ax = 0
            velocity = 0

        debug(f"velocity: {velocity}, ax: {ax}")
        velocity += ax

        # Limit speed
        velocity = min(velocity, MAX_SPEED)

        # If stopped
        # if velocity < 0: velocity = 0
        if (velocity == 0): continue
        

        # Update world
        # for i in range(0, velocity):
        if (velocity >= 1):
            foreground.pop(0)
            if (random.randint(0, 5) ==  1):
                foreground.append(CACTUS_CHAR)
            else:
                foreground.append(RAIL_CHAR)

            total_km += 0.01 # TODO: adjust


        # Render
        # debug(f"vel: {velocity:.4f}, ax: {ax}")
        # TODO: put in update if-check?
        render()


        # Sleep
        time.sleep(cur_time + DELAY - time.time())


        # Background (parallax)
        # background.pop(0)
        # if (random.randint(0, 20) == 1):
        #     background.append("🏔️")
        # else:
        #     background.append(None)
                   


if __name__ == "__main__":
    run()