#!/usr/bin/env python3

import datetime


def current_datetime():
    return datetime.datetime.now().strftime('%f_%S_%H_%M_%d_%m_%Y')