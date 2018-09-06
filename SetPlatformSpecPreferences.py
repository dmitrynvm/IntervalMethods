# -*- coding: cp1251

from PyQt4.QtCore import *
from PyQt4.QtGui import *

def SetPlatformSpecPreferences():
    # Кодировка символов.
    codec = QTextCodec.codecForName('CP-1251')
    QTextCodec.setCodecForCStrings(codec)
    QTextCodec.setCodecForLocale(codec)
    QTextCodec.setCodecForTr(codec)  