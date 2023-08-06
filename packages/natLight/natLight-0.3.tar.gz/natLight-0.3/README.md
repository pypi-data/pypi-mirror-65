## Description

This small python script outputs an 'white' RGB/ HSV value which varies depending on sunrise and sunset at your location as well on
your personal preferences regarding sleep and wake up times.

The project is intended to be used in a custom environment acting as "white light value provider".
In my case it's used to modify the RGB value of my room light to a more eye-friendly, warmer light.
It's compareable to any blue-light filter for Displays but implemts only the color changes.

You can modify transition time as well as your personal color temperature limits and other preferences in a config file.


## Requirements

Requires Python >=3.6

Requires ConfigParser:

```
$ pip install ConfigParser
```

## Installation

Either directly via pip:

```
$ pip install natLight
```

... or ...

Dowload Zip, extract and install via pip:

```
$ pip install .
```

Upgrade via pip:

```
$ pip install . --upgrade
```

Copy the config.cfg file to the folder where your script using natLight is located.


## Usage

You can run the main method of the script (which displays Sunrise, Sunset, Time and RGB Value as well as a plot) via:

python natLight.py


In your python script, you can get the RGB or HSV values as Array using:

```python
import natLight

print natLight.getColor('rgb')
print natLight.getColor('hsv')
```

E.g. you can acces the values via:

```python
import natLight

rgb = natLight.getColor('rgb')

red = rgb['r']
green = rgb['g']
blue = rgb['b']
```

## Configuration

To adapt the behavior to your personal needs, edit the config.txt file.
The parameters will be read on every request made to the API, so make sure you don't send requests permanently.


COORDS				(Float): The location provided here will be used to calculate sunrise and sunset.

EARLIESTWAKEUPTIME	(Integer): Specify your earliest wake-up time as hour and minute.
EARLIESTSLEEPTIME	(Integer): Specify your earliest sleep time as hour and minute.

COLORLIMITS			(Integer): Specify the color limits for day and nighttime.

MORNINGTRANSTIME	(Intger): Increasing this value will increase the transition time frome Nightimecolor to Daytimecolor.
EVENINGTRANSTIME	(Integer): Increasing this value will increase the transition time frim Daytimecolor to Nightimecolor.

SUNEFFECT			(Float: (0..1)): Increasing these values will stretch the transition curve towards the sunrise/ sunset.

DRIVERPARAMETERS	(Float: (0..1)): Adapt theses values to your application to match specific driver behaviors. Decreasing the values will decrease the intensity of the specific color.

PLOTPARAMETERS		(Integer): Adapt these values to your cmd-line size for correct virtualization of the color curve


If not otherwise specified, the valid range of the parameters is the common range e.g. hour between 0..24 and m between 0..60.
You can play with these values to match your favourite behavior, but they are already set to the most common color curve per default.
Pay attention when adjusting these values: There is not always a fallback or recheck of the valid range.
It is therefore recommended to plot the color curve before firing this on a standalone system.


## Contributing

Credits go to Carlos Platoni (2015) for the Sunset and Sunrise calculation (http://thorpesoftware.com/calculating-sunrise-and-sunset/)
as well as to ShawnF (2014) for the Color Temp to RGB Conversion (http://www.tannerhelland.com/4435/convert-temperature-rgb-algorithm-code/)

## Licensing

This is intended to be used in custom environment and therefore can be modified, and used without any
restrictations.
There is absolutely no warrenty for any results when using this project.

## Documentation

Refer to this README