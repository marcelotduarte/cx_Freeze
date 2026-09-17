#!/usr/bin/bash

FILENAME=$(winepath -u "$1")
gnome-screenshot --file="$FILENAME"
