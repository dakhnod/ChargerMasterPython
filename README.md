# ChargerMasterPythonClient
Python Library for controlling Charger Master compatible battery chargers

## Motivation
I want to make my chargers (SkyRC Q200) controllable via USB for remote controlling etc.
Thus, I reverse engineered the USB protocol and created this library.
I currently only tested with my own charger, so others may not work.
Specifically, I suppose that simpler chargers only have port 0 accessible.
Whatever, we'll take of it when the time comes.

## Example
just check out [main.py](main.py), which is currently an example script to control my Q200 charger.


## Disclaimer
I am not supported by any Charger company, so use the code at your own risk.
I do not take any responsibility for any chargers behaviour.