__all__ = ["AmLEInterface"]

import os
import sys
import warnings
import platform
from enum import Enum

import numpy as np

from ctypes import c_int, c_void_p, c_char_p, c_long, c_bool, cdll, sizeof
from numpy.ctypeslib import as_ctypes

supported_games_dict = {
    "Arkanoid": 0,
    "BuggyBoy": 1
}

DLL32 = "DLL/32Bit/"
DLL64 = "DLL/64Bit/"

def _load_cdll(path, name):
    relPath = ""
    if sys.platform.startswith("linux"):
        ext_suffix = ".so"
    elif sys.platform.startswith("darwin"):
        ext_suffix = ".dylib"
    elif sys.platform.startswith("win"):
        if(sizeof(c_void_p) == 4):
            os.add_dll_directory(os.path.dirname(__file__) + "/" + DLL32)
            ext_suffix = "-32.dll"
            relPath = DLL32
        else:
            os.add_dll_directory(os.path.dirname(__file__) + "/" + DLL64)
            ext_suffix = "-64.dll"
            relPath = DLL64
    else:
        raise RuntimeError(
            'Platform "{}" not recognized while trying to resolve shared library'.format(
                sys.platform))

    library_format = "{}{}{}" if platform.system() == "Windows" else "{}lib{}{}"
    library_path = os.path.join(path, library_format.format(relPath, name, ext_suffix))

    try:
        return cdll.LoadLibrary(library_path)
    except Exception as ex:
        raise RuntimeError(
            "Failed to load library {}. Attempted to load {}.\n{}".format(
                name, library_path, ex))



amle_lib = _load_cdll(os.path.dirname(__file__), "amle_c")


amle_lib.AmLE_new.argtypes = [c_char_p]
amle_lib.AmLE_new.restype = c_void_p

amle_lib.AmLE_del.argtypes = [c_void_p]
amle_lib.AmLE_del.restype = None

amle_lib.loadROM.argtypes = [c_void_p, c_int, c_char_p]
amle_lib.loadROM.restype = None

amle_lib.act.argtypes = [c_void_p, c_int]
amle_lib.act.restype = c_int

amle_lib.resetGame.argtypes = [c_void_p]
amle_lib.resetGame.restype = None

amle_lib.loadSnapshot.argtypes = [c_void_p, c_int, c_char_p]
amle_lib.loadSnapshot.restype = None

amle_lib.saveSnapshot.argtypes = [c_void_p, c_char_p]
amle_lib.saveSnapshot.restype = None

amle_lib.getNbLives.argtypes = [c_void_p]
amle_lib.getNbLives.restype = c_int

amle_lib.gameOver.argtypes = [c_void_p]
amle_lib.gameOver.restype = c_bool

amle_lib.getScore.argtypes = [c_void_p]
amle_lib.getScore.restype = c_int

amle_lib.getFrameNumber.argtypes = [c_void_p]
amle_lib.getFrameNumber.restype = c_long

amle_lib.getLegalActions.argtypes = [c_void_p, c_void_p]
amle_lib.getLegalActions.restype = None

amle_lib.getNbLegalActions.argtypes = [c_void_p]
amle_lib.getNbLegalActions.restype = c_int

amle_lib.getRGBScreen.argtypes = [c_void_p, c_void_p]
amle_lib.getRGBScreen.restype = None

amle_lib.getScreenWidth.argtypes = [c_void_p]
amle_lib.getScreenWidth.restype = c_int

amle_lib.getScreenHeight.argtypes = [c_void_p]
amle_lib.getScreenHeight.restype = c_int

amle_lib.step.argtypes = [c_void_p]
amle_lib.step.restype = None


def _str_as_bytes(arg):
    if isinstance(arg, str):
        return arg.encode("utf-8")
    return arg


class AmLEInterface(object):

    def __init__(self):
        path = _str_as_bytes(os.path.dirname(os.path.realpath(__file__)) + "/data")
        self.obj = amle_lib.AmLE_new(path)

    def loadROM(self, game, path):
        if game in supported_games_dict:
            amle_lib.loadROM(self.obj, supported_games_dict[game], path)
        else:
            print("No game named " + str(game)) 
        
    def act(self, event):
        return amle_lib.act(self.obj, event)

    def resetGame(self):
        amle_lib.resetGame(self.obj)

    def loadSnapshot(self, game, path):
        if game in supported_games_dict:
            amle_lib.loadSnapshot(self.obj, supported_games_dict[game], path)
        else:
            print("No game named " + str(game))

    def saveSnapshot(self, path):
        amle_lib.saveSnapshot(self.obj, path)
    
    def getNbLives(self):
        return amle_lib.getNbLives(self.obj)

    def gameOver(self):
        return amle_lib.gameOver(self.obj)
    
    def getScore(self):
        return amle_lib.getScore(self.obj)

    def getFrameNumber(self):
        return amle_lib.getFrameNumber(self.obj)
    
    def getLegalActions(self, tbl):
        amle_lib.getLegalActions(self.obj, as_ctypes(tbl))
        
    def getNbLegalActions(self):
        return amle_lib.getNbLegalActions(self.obj)
    
    def getScreen(self, tbl):
        amle_lib.getRGBScreen(self.obj, as_ctypes(tbl))
    
    def getScreenWidth(self):
        return amle_lib.getScreenWidth(self.obj)
    
    def getScreenHeight(self):
        return amle_lib.getScreenHeight(self.obj)

    def step(self):
        amle_lib.step(self.obj)

    def __del__(self):
        amle_lib.AmLE_del(self.obj)