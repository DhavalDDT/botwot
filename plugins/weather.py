import pyowm

from pyaib.plugins import keyword, plugin_class
from pyaib.db import db_driver

@plugin_class
class Weather(object):
	def __init__(self, context, config):
		self.owm = pyowm.OWM()
	
	
	def calculate_direction(self, degree):
		""" determine a compass direction based on numeric degrees """
		
		direction = " "
		if       0 <= degree <  22.5: direction = " N"
		elif  22.5 <= degree <  67.5: direction = " NE"
		elif  67.5 <= degree < 112.5: direction = " E"
		elif 112.5 <= degree < 157.5: direction = " SE"
		elif 157.5 <= degree < 202.5: direction = " S"
		elif 202.5 <= degree < 247.5: direction = " SW"
		elif 247.5 <= degree < 292.5: direction = " W"
		elif 292.5 <= degree < 337.5: direction = " NW"
		elif 337.5 <= degree <=  360: direction = " N"
		
		return direction
	
	
	@keyword("weather")
	def keyword_weather(self, context, msg, trigger, args, kargs):
		""" check the weather """
		
		# figure out first who to target and what the query is
		target_user = ""
		query = ""
		if len(args) >= 3 and args[-2] == "|":
			target_user = args[-1]
			query = " ".join(args[:-2])
		else:
			target_user = msg.sender
			query = " ".join(args)
		
		# figure out the units
		units = ["fahrenheit", u"\N{DEGREE SIGN}F"]
		if "c" in kargs:
			units = ["celsius", u"\N{DEGREE SIGN}C"]
		elif "k" in kargs:
			units = ["kelvin", "K"]
		
		observation = self.owm.weather_at_place(str(query))
		
		if observation:
			weather = observation.get_weather()
			
			msg.reply("%s: Conditions for %s: %s%s, %s, %s%% humidity, wind %sMPH%s" % (
					target_user or msg.sender,
					query, 
					weather.get_temperature(units[0])['temp'],
					units[1],
					weather.get_detailed_status(),
					weather.get_humidity(),
					weather.get_wind()['speed'],
					self.calculate_direction(weather.get_wind()['deg'])
					)
				)

			

