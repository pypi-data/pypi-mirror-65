# Rocket-pi

[![N|Solid](https://avatars3.githubusercontent.com/u/9026172?s=460&u=000a2f4b5787f6137255837f7acdfcb56ddd843e&v=4)]()
#### Copyright (c) 2020 Martin Shishkov - gulliversoft, licensed under GPL 3

## Remote open controll key enabling technology for RPI
Rocket is a user customizable remote control application intended mainly for electronics hobby projects.

Rocket connects 2 wheel drive remote control via WiFi (TCP). The network can be either in AP mode or STA mode. Using the APP you can control all movement directions plus arm and tool servos. In STA mode, your hobby target is a real Internet of Things device and can be controlled through WAN and LAN remotely.

>Disclaimer: Don't use Rocket for life support systems or any other situations where system failure may affect user or environmental safety. Please don't use Rocket in projects where high-level security is required. 

All the commands send from Rocket are text strings, ending with command ending CR (carriage return), ASCII 13 which is hex code 0x4.
All required adjustments and command interpretations are stored and done in python.
Probably you will need to adapt the Rocket to meet the requirements of your hobby project. In that case you will need python knowledge regarding script and direction converter module adaptation.
Bundling webiopi as core component enforces the use of Raspberry PI Zero, 2 or 3.
In general Rocket depends, demands and uses webiopi server on target side. Each button on the App screen uses webiopi macros to achieve the functionality behind. 
These macros are custom Pythons functions automatically bound to the REST API, so they are remotely callable. They allow to remotely trigger complex computation on the Raspberry Pi or manual events, trigger multiple GPIO at the same time or even change device settings.
In the current release V1.0, Rocket UI is limited to hardcoded range of 12 available @webiopi.macro calls:

| Command | Description |
| --- | --- |
| Forward() | void |
| TurnLeft()  | void |
| Reverse() | void |
| TurnRight() | void |
| Stop() | void |
| ArmUp() | void |
| ArmDown() | void |
| TiltUp() | void |
| TiltDown() | void |
| Lights() | void |
| FlashAll() | void |
| Move() | void, short int, short int |


