#!/bin/bash

# make CapsLock behave like Ctrl:
setxkbmap -option ctrl:nocaps

# make short-pressed Ctrl behave like Escape:
pkill -9 xcape
xcape -e 'Control_L=Escape;Shift_L=parenleft;Shift_R=parenright'
