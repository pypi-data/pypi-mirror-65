# -*- coding: utf-8 -*-

from cyrating.api import Cyrating

__author__ = 'Cyrating'
__email__ = 'tech@cyrating.com'
__version__ = '0.0.8'

__all__ = ["api"]


def init(**kwargs):
  return Cyrating(**kwargs)
