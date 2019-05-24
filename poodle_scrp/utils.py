#!/usr/bin/env python3

import datetime


def current_datetime():
    return datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')