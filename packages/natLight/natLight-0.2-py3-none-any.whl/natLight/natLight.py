#!/usr/bin/env python

# //////////////////////////////////////////////////////////////////////////
# /*
# Titel:				Python Natural Light 2 RGB Converter
# Author:				Melvin Strobl
# Credits:				Carlos Platoni (2015) : Sunset and Sunrise calculation
# 						http://thorpesoftware.com/calculating-sunrise-and-sunset/
# 						ShawnF (2014) : Color Temp to RGB Conversion :
# 						http://www.tannerhelland.com/4435/convert-temperature-rgb-algorithm-code/
# 						!! There may be modifications on the code stated above !!
# Date Created:			05.06.18
# Last Update: 			17.06.18

#BEGIN INIT INFO
# Provides:		Natural Light to RGB Converter
# Description:	Converts White to a more natural light in RGB
#END INIT INFO


# DISCLAIMER:
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# */
# //////////////////////////////////////////////////////////////////////////


#--------------------------------------------------------------------------
#	Import REGION
#--------------------------------------------------------------------------
import math
import sys
import colorsys
# Pyhton 2 / 3 fallback
try:
	import configparser
except:
	import ConfigParser
from math import log
from datetime import date, timedelta, datetime, time, tzinfo


#--------------------------------------------------------------------------
#	Utilities for trigonometric calculations
#--------------------------------------------------------------------------
def sinrad(deg):
	return math.sin(deg * math.pi/180)

def cosrad(deg):
	return math.cos(deg * math.pi/180)

#--------------------------------------------------------------------------
#	Calculate Sunrise and Sunset from Julian Date
#--------------------------------------------------------------------------
def calculatetimefromjuliandate(julianDate):
	julianDate=julianDate+.5
	secs=int((julianDate-int(julianDate))*24*60*60+.5)
	mins=int(secs/60)
	hour=int(mins/60)
	return time(hour, mins % 60, secs % 60)

#--------------------------------------------------------------------------
#	Calculate Sunrise and Sunset
#--------------------------------------------------------------------------
def calcsunriseandsunset(date, coord):
	a=math.floor((14-date.month)/12)
	y = date.year+4800-a
	m = date.month+12*a -3
	julian_date=date.day+math.floor((153*m+2)/5)+365*y+math.floor(y/4)-math.floor(y/100)+math.floor(y/400)-32045

	longitude=coord['longitude'] #West
	latitude=coord['latitude'] #North

	nstar= (julian_date - 2451545.0 - 0.0009)-(longitude/360)
	n=round(nstar)
	jstar = 2451545.0+0.0009+(longitude/360) + n
	M=(357.5291+0.98560028*(jstar-2451545)) % 360
	c=(1.9148*sinrad(M))+(0.0200*sinrad(2*M))+(0.0003*sinrad(3*M))
	l=(M+102.9372+c+180) % 360
	jtransit = jstar + (0.0053 * sinrad(M)) - (0.0069 * sinrad(2 * l))
	delta=math.asin(sinrad(l) * sinrad(23.45))*180/math.pi
	H = math.acos((sinrad(-0.83)-sinrad(latitude)*sinrad(delta))/(cosrad(latitude)*cosrad(delta)))*180/math.pi
	jstarstar=2451545.0+0.0009+((H+longitude)/360)+n
	jset=jstarstar+(0.0053*sinrad(M))-(0.0069*sinrad(2*l))
	jrise=jtransit-(jset-jtransit)

	return {'sunrise':calculatetimefromjuliandate(jrise),
			'sunset':calculatetimefromjuliandate(jset)}

#--------------------------------------------------------------------------
#	Converts given color Temp in K into RGB
#--------------------------------------------------------------------------
def colorTemp2RGB(temp):
	temp = temp/100

	# Red
	if temp <= 66:
		red = 255
	else:
		red = temp - 60
		red = 329.698727446 * (red** -0.1332047592)

	# Green
	if temp <= 66:
		green = temp
		green = 99.4708025861 * log(green) - 161.1195681661
	else:
		green = temp - 60
		green = 288.1221695283 * (green** -0.0755148492)

	#Blue
	if temp >= 66:
		blue = 255
	else:
		if temp <= 19:
			blue = 0
		else:
			blue = temp - 10
			blue = 138.5177312231 * log(blue) - 305.0447927307


	return [red/255*DRIVERADJUST_R, green/255*DRIVERADJUST_G, blue/255*DRIVERADJUST_B]

#--------------------------------------------------------------------------
#	Converts given UTC Time into linear Time from 0 to 1
#--------------------------------------------------------------------------
def utc2lin(hr, min):
	linMin = min/60.0/24.0
	linHr = hr/24.0

	return (linHr+linMin)

#--------------------------------------------------------------------------
#	Calculates sine-wave transition with given parameters
#	linTime: current Time in linear scale
#	linMidTime: wake up or sleep time in linear scale
#	linTransTime: maximum transition time from maxTemp to minTemp or vv
#	maxTemp: upper limit for colorTemp
#	minTemp: lower limit for colorTemp
#--------------------------------------------------------------------------
def transition(linTime, linMidTime, linTransTime, maxTemp, minTemp, orientation):
	#mid value of max and min value
	aveTemp = minTemp + (maxTemp - minTemp)/2
	#scale factor for range of sine fct
	scaleTemp = (maxTemp - minTemp)/2
	#actual time which is given to the sine fct
	linScaledTime=((linTime-linMidTime)/linTransTime)*math.pi

	# 	   y-shift y-orientation y-scale           x scale
	return aveTemp+orientation*scaleTemp*math.sin(linScaledTime)

#--------------------------------------------------------------------------
#	Calculates Sunrise and Sunset time from class sun into linear time
#--------------------------------------------------------------------------
def adaptTime2Sun(linEventTime, linTransTime, beforeMidday):
	today=date.today()
	res = calcsunriseandsunset(today, COORDS)

	if beforeMidday:
		sunrise={'hr':res['sunrise'].hour, 'min':res['sunrise'].minute}

		linSunrise = utc2lin(sunrise['hr'], sunrise['min'])

		linEventTime = linEventTime - MORNINGSUNEFFECT*(linEventTime-linSunrise)
		linTransTime = linTransTime - MORNINGSUNEFFECT*(linEventTime-linSunrise)

	else:
		sunset={'hr':res['sunset'].hour, 'min':res['sunset'].minute}

		linSunset = utc2lin(sunset['hr'], sunset['min'])

		linEventTime = linEventTime - EVENINGSUNEFFECT*(linEventTime-linSunset)
		linTransTime = linTransTime - EVENINGSUNEFFECT*(linEventTime-linSunset)

	return {
		'linEvent':linEventTime,
		'linTrans':linTransTime
	}

#--------------------------------------------------------------------------
#	Calculates White RGB into a smoother color using Sunset and
#	Sunrise Information
#--------------------------------------------------------------------------
def time2Color(linTime):
	if(linTime < utc2lin(12,00)): #Before Midday
		linTransTime = utc2lin(MORNINGTRANSTIME['hr'], MORNINGTRANSTIME['min'])
		linWakeUpTime = utc2lin(EARLIESTWAKEUPTIME['hr'], EARLIESTWAKEUPTIME['min'])

		linWakeUpTime = adaptTime2Sun(linWakeUpTime, linTransTime, True)['linEvent']
		linTransTime = adaptTime2Sun(linWakeUpTime, linTransTime, True)['linTrans']

		if abs(linWakeUpTime - linTime) < linTransTime/2: #within transition zone
			color = transition(linTime, linWakeUpTime, linTransTime, DAYTIMECOLOR, NIGHTTIMECOLOR, +1)
		elif linTime < linWakeUpTime: #nighttime
			color = NIGHTTIMECOLOR
		else: #daytime
			color = DAYTIMECOLOR
	else: #After Midday
		linTransTime = utc2lin(EVENINGTRANSTIME['hr'], EVENINGTRANSTIME['min'])
		linSleepTime = utc2lin(EARLIESTSLEEPTIME['hr'], EARLIESTSLEEPTIME['min'])

		linSleepTime= adaptTime2Sun(linSleepTime, linTransTime, False)['linEvent']
		linTransTime = adaptTime2Sun(linSleepTime, linTransTime, False)['linTrans']

		if abs(linSleepTime - linTime) < linTransTime/2: #within transition zone
			color = transition(linTime, linSleepTime, linTransTime, DAYTIMECOLOR, NIGHTTIMECOLOR, -1)
		elif linTime < linSleepTime: #daytime
			color = DAYTIMECOLOR
		else: #nighttime
			color = NIGHTTIMECOLOR

	return color

#--------------------------------------------------------------------------
#	Load User Config from File
#--------------------------------------------------------------------------
def loadUserConfig():
	#TODO: Check if there is something more convenient
	try:
		config = configparser.ConfigParser()
	except:
		config = ConfigParser.ConfigParser()
	# config.readfp(open(r'config.txt'))
	config.read('config.cfg')

	global COORDS, EARLIESTWAKEUPTIME, EARLIESTSLEEPTIME, MORNINGTRANSTIME, EVENINGTRANSTIME, NIGHTTIMECOLOR, DAYTIMECOLOR, MORNINGSUNEFFECT, EVENINGSUNEFFECT, DRIVERADJUST_R, DRIVERADJUST_G, DRIVERADJUST_B, YAXISSCALE, XAXISSCALE

	COORDS = {'longitude':float(config.get('COORDS','longitude')),
			 'latitude':float(config.get('COORDS','latitude'))}

	EARLIESTWAKEUPTIME = {'hr':int(config.get('EARLIESTWAKEUPTIME','hr')),
						 'min':int(config.get('EARLIESTWAKEUPTIME','min'))}

	EARLIESTSLEEPTIME = {'hr':int(config.get('EARLIESTSLEEPTIME','hr')),
						'min':int(config.get('EARLIESTSLEEPTIME','min'))}

	MORNINGTRANSTIME = {'hr':int(config.get('MORNINGTRANSTIME', 'hr')),
						'min':int(config.get('MORNINGTRANSTIME', 'min'))}
	EVENINGTRANSTIME = {'hr':int(config.get('EVENINGTRANSTIME', 'hr')),
						'min':int(config.get('EVENINGTRANSTIME', 'min'))}

	NIGHTTIMECOLOR = int(config.get('COLORLIMITS','nighttime'))
	DAYTIMECOLOR = int(config.get('COLORLIMITS','daytime'))

	MORNINGSUNEFFECT = float(config.get('SUNEFFECT','morning'))
	EVENINGSUNEFFECT = float(config.get('SUNEFFECT','evening'))

	DRIVERADJUST_R = float(config.get('DRIVERPARAMETERS','r'))
	DRIVERADJUST_G = float(config.get('DRIVERPARAMETERS','g'))
	DRIVERADJUST_B = float(config.get('DRIVERPARAMETERS','b'))

	YAXISSCALE = int(config.get('PLOTPARAMETERS','y'))
	XAXISSCALE = int(config.get('PLOTPARAMETERS','X'))

#--------------------------------------------------------------------------
#	Plots curve based on current user data
#--------------------------------------------------------------------------
def printCurve():
	PRECISION=100
	linTime = 0
	data = []
	plot = "\nCurve:\n\n"

	#Get data with iterated time
	while (linTime < 1):
		data.append(time2Color(linTime))
		linTime=linTime+(1.0/XAXISSCALE)

	#iterate through temperature
	for l in range(0,YAXISSCALE+1):
		currTemp=int(DAYTIMECOLOR-(DAYTIMECOLOR-NIGHTTIMECOLOR)/YAXISSCALE*l)
		plot = plot+str(currTemp)+"\t|"

		#iterate through time
		for c in range(0,XAXISSCALE-1):
			#if value matches
			if(data[c]/PRECISION>=currTemp/PRECISION):
				plot = plot+"-"
			else:
				plot = plot+" "
		plot = plot+"\n"
	plot=plot+"\t"

	#add time axis
	for c in range(0,XAXISSCALE+1):
		plot = plot+"_"

	#add placeholder
	plot = plot+"\n\t "
	div=XAXISSCALE/24
	c=0
	time=0

	#add time caption
	while(c<XAXISSCALE):
		if(c==int(div*time)):
			plot = plot+str(time)
			if(time<10):
				plot=plot+" "
			time=time+1
		elif(c<div*time-2):
			plot=plot+" "
		c=c+1

	#print all
	print(plot)

#--------------------------------------------------------------------------
#	Returning function for package usage
#--------------------------------------------------------------------------
def convert2RGB():
	now = datetime.now()

	return colorTemp2RGB(time2Color(utc2lin(now.hour, now.minute)))

def convert2HSV():
	now = datetime.now()
	rgb = colorTemp2RGB(time2Color(utc2lin(now.hour, now.minute)))

	return colorsys.rgb_to_hsv(rgb[0],rgb[1],rgb[2])

def getColor(colorSpace):
	loadUserConfig()

	if(colorSpace == 'hsv'):
		return convert2HSV()
	else:
		return convert2RGB()

#--------------------------------------------------------------------------
#	Main
#--------------------------------------------------------------------------
def main():
	loadUserConfig()

	today=date.today()
	res = calcsunriseandsunset(today, COORDS)
	print("Sunrise at:\t"+str(res['sunrise']))
	print("Sunset at:\t"+str(res['sunset']))

	now = datetime.now()
	print("Current Time:\t"+str(now.hour)+":"+str(now.minute))

	color = time2Color(utc2lin(now.hour, now.minute))
	print("Calculated Color Temperature:\t"+str(color))

	rgb = colorTemp2RGB(color)

	print("Red:\t"+str(rgb[0])+"\nGreen:\t"+str(rgb[1])+"\nBlue:\t"+str(rgb[2]))

	printCurve()


if __name__ == '__main__':

	if(len(sys.argv)>1 and sys.argv[1] == '-d'):
		main()
	else:
		try:
			main()
		#On keyboard interrupt
		except KeyboardInterrupt:
			print("\nQuit cause of keyboard interrupt")
			# quit_i2c_broker()

		#On IO Error interrupt
		except IOError:
			print("\nQuit cause of IO error")
			# quit_i2c_broker()
		#General Errors
		except:
			e = sys.exc_info()[0]
			print( "<p>Error: %s</p>" % e )