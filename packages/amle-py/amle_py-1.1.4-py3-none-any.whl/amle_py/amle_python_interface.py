__all__ = ["AmLEInterface"]

import os
import sys
import warnings
import platform
from enum import Enum

import numpy as np

from ctypes import c_int, c_uint, c_void_p, c_char_p, c_long, c_bool, cdll, sizeof
from numpy.ctypeslib import as_ctypes

supported_games_dict = {
    "Arkanoid": 0,
    "BuggyBoy": 1
}

DLL32 = "DLL/32Bit/"
DLL64 = "DLL/64Bit/"
DATA_PATH = "/data/"

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

amle_lib.setEmulatorSpeed.argtypes = [c_void_p, c_int]
amle_lib.setEmulatorSpeed.restype = None

amle_lib.pokeMemory.argtypes = [c_void_p, c_uint, c_int]
amle_lib.pokeMemory.restype = c_bool

amle_lib.toggleSound.argtypes = [c_void_p, c_bool]
amle_lib.toggleSound.restype = None

amle_lib.step.argtypes = [c_void_p]
amle_lib.step.restype = None


def _str_as_bytes(arg):
    if isinstance(arg, str):
        return arg.encode("utf-8")
    return arg

class AmLEInterface(object):
    '''
    This class is using the methods of the AmLEInterface C class. It is used to 
    interact with an Amstrad CPC emulator (Caprice32).
    '''
    def __init__(self):
        '''
        Creates a new AmLE object, which coreponds to starting the emulator.
        '''
        path = _str_as_bytes(os.path.dirname(os.path.realpath(__file__)) + DATA_PATH)
        self.obj = amle_lib.AmLE_new(path)
        
    def getSupportedGames(self):
        '''
        This methods allows the user to know which games are available.
        
        :return: Returns a lis of string coresponding to the list of games you can
        use.
        '''
        # We make a list because we don't want the user to mess with the 
        games = []
        for key in supported_games_dict:
            games.append(key)
        return games

    def loadROM(self, game, path):
        '''
        This methods loads a .dsk file in memory. This method is highly deprecated.
        
        :param game: The name of the game to load. Use getSupportedGames to know which string are valid.
        :param path: The path to the game to load.
        '''
        # Simple check to make sure the game required exists
        if game in supported_games_dict:
            amle_lib.loadROM(self.obj, supported_games_dict[game], path)
        else:
            print("No game named " + str(game)) 
        
    def act(self, event):
        '''
        Sends an input to the emulator.
        
        :param event: An int representing an event within the AmLE. getLegalActions should be used 
        to get the integers to give for the current game.
        '''
        return amle_lib.act(self.obj, event)

    def resetGame(self):
        '''
        Resets the current game to its original state. If a snapshot was loaded, it will go back to 
        the start of the snapshot, so this is not an absolute reset of the game. If no game is loaded 
        then the emulator restarts.
        '''
        amle_lib.resetGame(self.obj)

    def loadSnapshot(self, game, path):
        '''
        Loads a snapshot in memory. This is the method that should be used to start a game.
        
        :param game: The name of the game to load. Use getSupportedGames to know which string are valid.
        :param path: The path to the game to load.
        '''
        if game in supported_games_dict:
            amle_lib.loadSnapshot(self.obj, supported_games_dict[game], path)
        else:
            print("No game named " + str(game))

    def saveSnapshot(self, path):
        '''
        Saves a snapshot of the current state of the current game.
        
        :param path: The path to the location in which the snapshot should be saved.
        '''
        amle_lib.saveSnapshot(self.obj, path)
    
    def getNbLives(self):
        '''
        Returns the current number of lives, if any. If the game does not contain a lives system, the value 
        is undefined.
        '''
        return amle_lib.getNbLives(self.obj)

    def gameOver(self):
        '''
        Returns true if the game has ended, false otherwise.
        '''
        return amle_lib.gameOver(self.obj)
    
    def getScore(self):
        '''
        Returns the current score of the game, if any. If the score does not contain any score, then the value 
        is undefined.
        '''
        return amle_lib.getScore(self.obj)

    def getFrameNumber(self):
        '''
        Returns the number of frames that happened since the emulator started (resets do NOT set this value to zero).
        '''
        return amle_lib.getFrameNumber(self.obj)
    
    def getLegalActions(self, tbl):
        '''
        Stores the set of legal actions of the current game in the given array.
        
        :param tbl: A numpy array that should be able to contain all the legal action. The size has to be set 
        before hand so use getNbLegalActions to create it. It should be defines as such :
        tbl = np.empty(getNbLegalActions(), dtype=np.int32)
        '''
        amle_lib.getLegalActions(self.obj, as_ctypes(tbl))
        
    def getNbLegalActions(self):
        '''
        Returns the number of legal actions for the current game.
        '''
        return amle_lib.getNbLegalActions(self.obj)
    
    def getScreen(self, tbl):
        '''
        Stores the list of pixels currently displayed in the given array.
        
        :param tbl: A numpy array that should be able to contain all the pixels. The size has to be set 
        before hand so use getScreenWidth and getScreenHeight to create it. It should be defines as such :
        tbl = np.empty(getScreenWidth() * getScreenHeight(), dtype=np.uint32)
        '''
        amle_lib.getRGBScreen(self.obj, as_ctypes(tbl))
    
    def getScreenWidth(self):
        '''
        Returns the width of the screen.
        '''
        return amle_lib.getScreenWidth(self.obj)
    
    def getScreenHeight(self):
        '''
        Returns the height of the screen.
        '''
        return amle_lib.getScreenHeight(self.obj)
    
    def setEmulatorSpeed(self, speed):
        '''
        Sets the speed of the emulator.
        
        :param speed: The speed at which the emulator should run. Default is 4. Min is 2 and max is 32. 
        Any incorrect value will set the emulator speed to its default value.
        '''
        amle_lib.setEmulatorSpeed(self.obj, speed)
        
    def pokeMemory(self, addr, value):
        '''
        Modifies the memory of the game at the given address with the given value.
        
        :param addr: The address to poke, it should be in range [0, 65535].
        :param value: The value to set the address to, it should be in range [-128, 255]
        '''
        amle_lib.pokeMemory(self.obj, addr, value)
        
    def toggleSound(self, value):
        '''
        Enables/disables sound.
        
        :param value: If true, the sound will be enabled, otherwise disabled.
        '''
        amle_lib.toggleSound(self.obj, value)

    def step(self):
        '''
        Makes a step in the emulation, goes to the next frame, applies effect of given actions.
        '''
        amle_lib.step(self.obj)

    def __del__(self):
        amle_lib.AmLE_del(self.obj)