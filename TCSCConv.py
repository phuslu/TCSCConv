#!/usr/bin/env python
#coding:utf-8

import sys, os, re
import ctypes

class TCSCConvert:
    def __init__(self, tosimp=True, byword=True):
        self.tosimp = tosimp
        self.byword = byword
    def __enter__(self):
        curdir = os.path.dirname(globals().get('__file__', sys.executable))
        if curdir not in os.environ['PATH']:
            os.environ['PATH'] += os.pathsep + curdir
        self.TCSCInitialize = ctypes.windll.MSTR2TSC.TCSCInitialize
        self.TCSCUninitialize = ctypes.windll.MSTR2TSC.TCSCUninitialize
        self.TCSCConvertText = ctypes.windll.MSTR2TSC.TCSCConvertText
        self.TCSCFreeConvertedText = ctypes.windll.MSTR2TSC.TCSCFreeConvertedText
        self.TCSCInitialize()
        return self
    def __exit__(self, type, value, traceback):
        return self.TCSCUninitialize()
    def __call__(self, text):
        ptr, num = ctypes.c_wchar_p(0), ctypes.c_int(0)
        self.TCSCConvertText(text, len(text), ctypes.byref(ptr), ctypes.byref(num), self.tosimp, not self.byword, True)
        out = ptr.value
        self.TCSCFreeConvertedText(ptr)
        return out

def test():
    with TCSCConvert(True, True) as convert:
        print convert(u'伺服器')

if __name__ == '__main__':
    test()
