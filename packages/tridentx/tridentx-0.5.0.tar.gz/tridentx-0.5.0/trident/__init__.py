from __future__ import absolute_import
import sys
from sys import  stderr
from importlib import reload
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)



__version__ = '0.5.0'
stderr.write('trident {0}\n'.format(__version__))
from .backend import *
from trident import models
from trident import misc
from trident import callbacks
from trident import data

import threading



