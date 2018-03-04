#!/usr/bin/env python3

import RPi.GPIO as GPIO
from os import listdir
from os.path import isfile, join, dirname, realpath
from pygame import mixer

SCRIPT_PATH = dirname(realpath(__file__))
SONG_PATH = SCRIPT_PATH + "/songs/"
GPIO_SIGNAL = 7
BOUNCE_TIME = 200
GPIO.setmode(GPIO.BOARD)
GPIO.setup(GPIO_SIGNAL, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

song_list = [f for f in listdir(SONG_PATH) if isfile(join(SONG_PATH, f))]
current_index = 0
mixer.init()

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
    player = mixer.Sound(file=song)
    player.play()
    while mixer.get_busy():
        pass

    update_index()


def launch_action():
    play_next_song()


def callback_gpio(channel):
    if GPIO.input(GPIO_SIGNAL):
        print("DING!")
        # ACTION
        launch_action()


if __name__ == '__main__':
    GPIO.add_event_detect(GPIO_SIGNAL, GPIO.RISING, callback=callback_gpio, bouncetime=BOUNCE_TIME)
    while True:
        pass
