/* *****************************************************************************
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License version 2
 * as published by the Free Software Foundation.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
 * *****************************************************************************
 * A.M.L.E (Amstrad Learning Environment)
 * Copyright (c) 2020 by Kévin Durou, Johann Kadionik, Vincent Ameeuw, Wilfried 
 * Augeard and Theo De Castro Pinto.
 * Released under the GNU General Public License; see License.txt for details.
 * 
 * A.L.E (Arcade Learning Environment)
 * Copyright (c) 2009-2013 by Yavar Naddaf, Joel Veness, Marc G. Bellemare and
 *   the Reinforcement Learning and Artificial Intelligence Laboratory
 * Released under the GNU General Public License; see License.txt for details.
 *
 * Based on: Caprice32  --  "An Amstrad CPC Emulator"
 * (c) Copyright 1997-2015 Ulrich Doewich
 * (c) Copyright 2016-2019 Colin Pitrat
 *
 * *****************************************************************************
 *  amle_c_wrapper.h
 *
 *  The shared library interface.
 **************************************************************************** */

#ifndef __AMLE_C_WRAPPER_H__
#define __AMLE_C_WRAPPER_H__

/**
 * \file amle_c_wrapper.h
 * \brief This file is a wrapper of all the functions created in the amle_interface.h file. It 
 * will then be used to create a C_LIB usable in Python.
 */ 

#include "amle_interface.h"
#include "CPCScreen.h"
#include <windows.h>

#ifdef BUILDING_EXAMPLE_DLL
#define EXAMPLE_DLL __declspec(dllexport)
#else
#define EXAMPLE_DLL __declspec(dllexport)
#endif

/**
 * \brief A C wrapper of all the methods of the AmLEInterface class. The code is directly in the .h file 
 * as expected. This file copies the model of the ALE wrapper.
 */ 
extern "C" {

    /**
     * \fn AmLEInterface *AmLE_new()
     * \brief Creates a new AmLEInterface object.
     * \param path: The path the python file is in.
     * \return The created object.
     */ 
    AmLEInterface * EXAMPLE_DLL AmLE_new(const char * path) {return new AmLEInterface(path);}
    
    /**
     * \fn void AmLE_del(AmLEInterface *amle)
     * \brief Deletes an AmLEInterface Object by calling its destructor.
     * \param amle: The object to destroy.
     */ 
    void EXAMPLE_DLL AmLE_del(AmLEInterface *amle) {delete amle;}

    /**
     * \fn void loadROM(AmLEInterface *amle, int game, const char * path)
     * \brief Loads a ROM in memory. This function is deprecated, it is not reliable. 
     * Prefer loadSnapshot.
     * \param amle: The AmLEInterface object to use to load the game into.
     * \param game: The game to load as an int. This int should correspond to a SupportedGames 
     * enum type.
     * \param path: The path to the game to load.
     * \deprecated Use loadSnapshot instead.
     */ 
    void EXAMPLE_DLL loadROM(AmLEInterface *amle, int game, const char * path) {
        amle->loadROM(static_cast<SupportedGames> (game), path);
    }

    /**
     * \fn int act(AmLEInterface *amle, int event_as_int)
     * \brief Sends an input to the emulator through the AmLEInterface object given.
     * \param amle: The AmLEInterface object to use to send the action into.
     * \param event_as_int: An SDL_Event as an int to apply. For the record the integer is 32 bits, 
     * the 16 left most bits correspond to the key pressed, the 8 next bits correspond to the mod to consider 
     * (whether ctrl, shift, etc... is pressed) and the 8 last bits are the type (pressed/released). The division 
     * is not optimal but is good enough to handle any SDL_Event.
     * \return The reward after the action was applied (how "good" of an action it was, this functionality is 
     * still under development).
     */ 
    int EXAMPLE_DLL act(AmLEInterface *amle, int event_as_int) {
        SDL_Event event;
        
        int key = event_as_int >> 16;
        event_as_int = event_as_int - (key << 16);

        int mod = event_as_int >> 8;
        event_as_int = event_as_int - (mod << 8);

        int type = event_as_int;

        event.type = type;
        event.key.keysym.mod = static_cast<SDLMod> (mod);
        event.key.keysym.sym = static_cast<SDLKey> (key);

        return amle->act(&event);
    }

    /**
     * \fn void resetGame(AmLEInterface *amle)
     * \brief Resets the current game to its initial state. If a snapshot was loaded, then it will go back 
     * to the start of this snapshot. If nothing was loaded before this command was used, the emulator will 
     * soft reset.
     * \param amle: The AmLEInterface object to use to reset the game.
     */ 
    void EXAMPLE_DLL resetGame(AmLEInterface *amle) {return amle->resetGame();}

    /**
     * \fn void loadSnapshot(AmLEInterface *amle, int game, const char * path)
     * \brief Loads a snapshot into memory.
     * \param amle: The AmLEInterface object to use to load the game into.
     * \param path: The path to the file of the game.
     */ 
    void EXAMPLE_DLL loadSnapshot(AmLEInterface *amle, int game, const char * path) {
        return amle->loadSnapshot(static_cast<SupportedGames> (game), path);
    }

    /**
     * \fn saveSnapshot(AmLEInterface *amle, const char * path)
     * \brief Save a snapshot of the current state of the memory of the emulator in a file .sna.
     * \param amle: The AmLEInterface object to use to save the snapshot from.
     * \param path: The path to the location where the snapshot should be saved.
     */ 
    void EXAMPLE_DLL saveSnapshot(AmLEInterface *amle, const char * path) {return amle->saveSnapshot(path);}

    /**
     * \fn int getNbLives(AmLEInterface *amle)
     * \brief Returns the current number of lives, if any.
     * \param amle: The AmLEInterface object to use to find the number of lives into.
     * \return The current number of lives found. 
     */ 
    int EXAMPLE_DLL getNbLives(AmLEInterface *amle) {return amle->getNbLives();}


    /**
     * \fn bool gameOver(AmLEInterface *amle)
     * \brief Determines if the game has ended.
     * \param amle: The AmLEInterface object to use to determine whether the game has ended or not.
     * \return True if the game has ended, false otherwise.
     */ 
    bool EXAMPLE_DLL gameOver(AmLEInterface *amle) {return amle->gameOver();}

    /**
     * \fn int getScore(AmLEInterface *amle)
     * \brief Returns teh current score of the game, if any.
     * \param amle: The AmLEInterface object to use to find the score into.
     * \return The current score found.
     */ 
    int EXAMPLE_DLL getScore(AmLEInterface *amle) {return amle->getScore();}

    /**
     * \fn void getLegalActions(AmLEInterface *amle, int * actions)
     * \brief Stores the list of legal actions available in the current game in the given array.
     * \param amle: The AmLEInterface object to use to find the legal actions.
     * \param actions: The array to store the actions as integer into. The integers correspond to 
     * SDL_Events. For the record the integer is 32 bits, the 16 left most bits correspond to the key pressed, 
     * the 8 next bits correspond to the mod to consider (whether ctrl, shift, etc... is pressed) and the 8 last 
     * bits are the type (pressed/released). The division is not optimal but is good enough to handle any SDL_Event.
     */ 
    void EXAMPLE_DLL getLegalActions(AmLEInterface *amle, int * actions) {
        std::vector<SDL_Event> events = amle->getLegalActions();

        for(unsigned int index = 0; index < events.size(); index++)
        {
            int event_as_int = 0;
            SDL_Event event = events[index];

            event_as_int = static_cast<int> (event.key.keysym.sym);
            event_as_int = (event_as_int << 8) + event.key.keysym.mod;
            event_as_int = (event_as_int << 8) + event.type;

            actions[index] = event_as_int;
        }
    }

    /**
     * \fn int getNbLegalActions(AmLEInterface * amle)
     * \brief Returns the total number of legal actions in this game.
     * \param amle: The AmLEInterface object to use to find this number.
     * \return The total number of legal actions in this game.
     */ 
    int EXAMPLE_DLL getNbLegalActions(AmLEInterface * amle) {
        return amle->getLegalActions().size();
    }

    /**
     * \fn long getFrameNumber(AmLEInterface *amle)
     * \brief Returns the total number of frames that passed since th emulator started.
     * \param amle: The AmLEInterface object to use to find this number.
     * \return The total number of frames that passed since the emulator started.
     */ 
    long EXAMPLE_DLL getFrameNumber(AmLEInterface *amle) {return amle->getFrameNumber();}

    /**
     * \fn void getRGBScreen(AmLEInterface *amle, unsigned int * screen_data)
     * \brief Stores the list of pixels currently displayed into the given array. Pixels stored are 
     * 32 bits long unsigend integer, therefore 8 consecutive bits correspond to one composent of the 
     * pixel.
     * \param amle: The AmLEInterface to use to find the screen in.
     * \param screen_data: The array to store the pixels in, it should already have been initialized 
     * with the correct size.
     */ 
    void EXAMPLE_DLL getRGBScreen(AmLEInterface *amle, unsigned int * screen_data) {
        CPCScreen screen = amle->getRGBScreen();
        int width = screen.width;
        int height = screen.height;

        for(int line = 0; line < height; line++) {
            for(int column = 0; column < width; column++) {
                screen_data[line * width + column] = screen.pixels[line * width + column];
            }
        }
    }

    /**
     * \fn int getScreenWidth(AmLEInterface * amle)
     * \brief Returns the width of the screen.
     * \param amle: The AmLEInterface object to use to find the value in.
     * \return The width of the screen.
     */ 
    int EXAMPLE_DLL getScreenWidth(AmLEInterface * amle) {
        return amle->getRGBScreen().width;
    }

    /**
     * \fn int getScreenHeight(AmLEInterface * amle)
     * \brief Returns the height of the screen.
     * \param amle: The AmLEInterface object to use to find the value in.
     * \return The height of the screen.
     */ 
    int EXAMPLE_DLL getScreenHeight(AmLEInterface * amle) {
        return amle->getRGBScreen().height;
    }

    /**
     * \fn void step(AmLEInterface *amle)
     * \brief Executes the next frame.
     * \param amle: The AmLEInterface object to use to execute the next frame in.
     */ 
    void EXAMPLE_DLL step(AmLEInterface *amle) {return amle->step();}

}

#endif