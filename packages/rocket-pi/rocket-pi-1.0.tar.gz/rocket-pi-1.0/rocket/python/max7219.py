# +---------------------------------------------------------------------------+
#
#      Program:    max7219.py
#
#      Purpose:    Example, controlling max7219 led matrix over the web            
#      
#      Target:     ARMV61A
#
#      Author:     Martin Shishkov
#
#      License:    GPL 3
#######DEMO####################################################################
#      git clone https://github.com/coding-world/max7219
#      cd max7219
#      sudo apt-get install python-dev
#      sudo pip3 install spidev
#      sudo python setup.py install
# +---------------------------------------------------------------------------+

import webiopi
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'modules'))


import max7219.led as led
matrix = led.matrix()


 
# setup function is automatically called at WebIOPi startup
def setup():
    matrix.brightness(5)

# loop function is repeatedly called by WebIOPi 
def loop():
    webiopi.sleep(1)   

# destroy function is called at WebIOPi shutdown
def destroy():
    matrix.brightness(0)

@webiopi.macro
def Forward():
    value = ord("U");
    matrix.letter(0, value)

@webiopi.macro
def TurnLeft():
    value = ord("L");
    matrix.letter(0, value)

@webiopi.macro
def Reverse():
    value = ord("D");
    matrix.letter(0, value)

@webiopi.macro
def TurnRight():
    value = ord("K");
    matrix.letter(0, value)

@webiopi.macro
def Stop():
    value = ord("R");
    matrix.letter(0, value)   

@webiopi.macro
def ArmUp():
    value = ord("X");
    matrix.letter(0, value)
    
@webiopi.macro
def ArmDown():
    value = ord("Y");
    matrix.letter(0, value)    
    
@webiopi.macro
def TiltUp():
    value = ord("F");
    matrix.letter(0, value)  
    
@webiopi.macro
def TiltDown():
    value = ord("G");
    matrix.letter(0, value)
    
@webiopi.macro
def Lights():
    value = ord("A");
    matrix.letter(0, value)

@webiopi.macro
def FlashAll():
    matrix.show_message("rocket")
    
@webiopi.macro    
def Move(L, R):
    matrix.letter(0, ord(L))
    matrix.letter(1, ord(R))  
