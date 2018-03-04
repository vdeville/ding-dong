#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
from os import listdir
from os.path import isfile, join, dirname, realpath
from pygame import mixer

SCRIPT_PATH = dirname(realpath(__file__))
SONG_PATH = SCRIPT_PATH + "/songs/"
GPIO_SIGNAL = 7
BOUNCE_TIME = 200
MIN_SOUND_TIME = 4
GPIO.setmode(GPIO.BOARD)
GPIO.setup(GPIO_SIGNAL, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
mixer.init()

song_list = [f for f in listdir(SONG_PATH) if isfile(join(SONG_PATH, f))]
current_index = 0


def update_index():
    global current_index
    if current_index >= len(song_list) - 1:
        current_index = 0
    else:
        current_index += 1


def play_next_song():
    song = SONG_PATH + song_list[current_index]
    print("Index: " + str(current_index))
    print("Playing: " + song)
    sound = mixer.Sound(file=song)
    sound.play()

    while mixer.get_busy():
        pass
    # Fix for small song. If default song of "ding" is biggest than custom song
    if sound.get_length() < MIN_SOUND_TIME:
        print("Original song not finish, waiting " + str(MIN_SOUND_TIME - sound.get_length()) + "s more")
        time.sleep(MIN_SOUND_TIME - sound.get_length())

    update_index()


def launch_action():
    play_next_song()


def callback_gpio(channel):
    if GPIO.input(GPIO_SIGNAL):
        print("DING!")
        # ACTION
        launch_action()


if __name__ == '__main__':
    try:
        GPIO.add_event_detect(GPIO_SIGNAL, GPIO.RISING, callback=callback_gpio, bouncetime=BOUNCE_TIME)
        while True:
            pass
    except KeyboardInterrupt:
        print("Bye!")
