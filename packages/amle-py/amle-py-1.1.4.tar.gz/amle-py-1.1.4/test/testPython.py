# In this file we do NOT need to test if every method does what it should do
# This is tested with the cpp files. Here we test if the Wrapper has been correctly done
# That is, are all methods well defined with the correct types

import sys
import numpy as np
import random

sys.path.insert(0, "../amle_py/")

import amle_python_interface as api 

amle = api.AmLEInterface()

amle.toggleSound(False)
amle.setEmulatorSpeed(32)

amle.loadSnapshot("Arkanoid", b"snap/arka.sna")
amle.saveSnapshot(b"build/test.sna")

nbLegalActions = amle.getNbLegalActions()
legalActions = np.empty(nbLegalActions, dtype=np.int32)
amle.getLegalActions(legalActions)
legalActions = legalActions.tolist()

width = amle.getScreenHeight()
height = amle.getScreenWidth()
screen = np.empty(width * height, dtype=np.uint32)
amle.getScreen(screen)

amle.getNbLives()
amle.getScore()

amle.act(random.choice(legalActions))
amle.step()

amle.getFrameNumber()
amle.resetGame()
amle.pokeMemory(0xb7d4, 6)
amle.gameOver()

print("The wrapper has been correctly done.")
