i# A simple yet effective python package to check whether a given year is leap or not
# Leap Year Conditions
# A year x is a leap year if either 1) or 2) is true 
# 1) if x is divisible by 4 and not divisible by 100. 
# 2) if x is divisible by 4 and divisible by 400.  

def calc_leap(year):
	try: 
		if type(year) is str or type(year) is float:
			year = int(year)
	except ValueError:
		year = int(float(year))	
	return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def isleap(obj):
	try:
		iter_obj = iter(obj)  
		if type(obj) is list:
			return [calc_leap(x) for x in obj]
		elif type(obj) is tuple:
			return tuple([calc_leap(x) for x in obj])
		elif type(obj) is str: 
			return calc_leap(obj) 
		else:
			return False   
	except TypeError:
		return calc_leap(obj)
