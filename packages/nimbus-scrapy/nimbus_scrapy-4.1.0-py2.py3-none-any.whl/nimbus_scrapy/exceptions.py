# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division, unicode_literals


class CrawledItemError(Exception):
    """Drop item from the item pipeline"""
    pass


class ScrapItemError(Exception):
    """Drop item from the item pipeline"""
    pass
