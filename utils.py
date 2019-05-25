#!/usr/bin/env python3

import datetime
import re


def current_datetime():
    return datetime.datetime.now().strftime('%f_%S_%H_%M_%d_%m_%Y')


def computerise_string(s):
    """Transform a string into alphanumeric underscore-separated lowercase words"""
    return '_'.join(re.sub(r'[^a-zA-Z0-9\s]+', '', s).split()).lower()