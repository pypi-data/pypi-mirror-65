#!/usr/bin/python
# -*- coding: utf-8 -*-

from pytplot import get_data


def data_exists(tvar):
    data = get_data(tvar)
    if data:
        return True
    return False
