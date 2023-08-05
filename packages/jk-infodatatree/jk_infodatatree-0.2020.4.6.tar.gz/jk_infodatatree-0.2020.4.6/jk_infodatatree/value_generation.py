

import datetime

import jk_flexdata
from jk_testing import Assert





def toV(value, dataType:str = None, defaultType:str = None) -> jk_flexdata.FlexObject:
	if dataType is None:
		# autodetect type
		if value is None:
			# try to accept the default type
			if defaultType is None:
				raise Exception("Value is None and default type is not set!")
			assert defaultType in [ "int", "str", "bool", "float", "int[]", "str[]", "float[]", "tempc", "timestamputc", "timestamp", "duration", "bytes", "freq", "secsdiff" ]
			dataType = defaultType
		elif isinstance(value, bool):
			dataType = "bool"
		elif isinstance(value, int):
			dataType = "int"
		elif isinstance(value, float):
			dataType = "float"
		elif isinstance(value, str):
			dataType = "str"
		elif isinstance(value, list):
			nCountStr = 0
			nCountInt = 0
			nCountFloat = 0
			for item in value:
				if isinstance(item, float):
					nCountFloat += 1
				elif isinstance(item, int):
					nCountInt += 1
				elif isinstance(item, str):
					nCountStr += 1
				else:
					raise Exception("Unknown list item data type: " + repr(type(item)))
			if nCountInt == nCountFloat == nCountStr == 0:
				# assume it is a string lst
				dataType = "str[]"
			elif (nCountInt * nCountFloat != 0) or (nCountInt * nCountStr != 0) or (nCountFloat * nCountStr != 0):
				raise Exception("List with mixed item types!")
			else:
				if nCountFloat > 0:
					dataType = "float[]"
				elif nCountInt > 0:
					dataType = "int[]"
				else:
					dataType = "str[]"
		else:
			raise Exception("Unknown data type: " + repr(type(value)))

	else:
		# type has been specified
		if value is None:
			# accept the type as it is
			pass
		elif dataType == "bool":
			Assert.isInstance(value, bool)
		elif dataType == "int":
			Assert.isInstance(value, int)
		elif dataType == "float":
			Assert.isInstance(value, float)
		elif dataType == "str":
			Assert.isInstance(value, str)
		elif dataType == "tempc":
			Assert.isInstance(value, (int, float))
		elif dataType == "timestamputc":
			if isinstance(value, datetime.datetime):
				value = value.timestamp()
			else:
				Assert.isInstance(value, (int, float))
		elif dataType == "timestamp":
			if isinstance(value, datetime.datetime):
				value = value.timestamp()
			else:
				Assert.isInstance(value, (int, float))
		elif dataType == "duration":
			Assert.isInstance(value, (int, float))
		elif dataType == "bytes":
			Assert.isInstance(value, int)
		elif dataType == "freq":
			Assert.isInstance(value, (int, float))
		elif dataType == "secsdiff":
			Assert.isInstance(value, (int, float))
		else:
			raise Exception("Invalid data type: " + repr(dataType))

	return jk_flexdata.FlexObject({
		"dt": dataType,
		"v": value
	})
#

def toVTemperature(value) -> jk_flexdata.FlexObject:
	return toV(value, "tempc")
#

def toVDurationSeconds(value) -> jk_flexdata.FlexObject:
	return toV(value, "duration")
#

def toVBytes(value) -> jk_flexdata.FlexObject:
	return toV(value, "bytes")
#

def toVTimestamp(value) -> jk_flexdata.FlexObject:
	return toV(value, "timestamp")
#

def toVStr(value) -> jk_flexdata.FlexObject:
	return toV(value, "str")
#

def toVFreqMHz(value) -> jk_flexdata.FlexObject:
	return toV(value * 1000000, "freq")
#

def toVDiffSeconds(value) -> jk_flexdata.FlexObject:
	return toV(value, "secsdiff")
#

def toVTimestampUTC(value) -> jk_flexdata.FlexObject:
	return toV(value, "timestamputc")
#

def toVUptime(value) -> jk_flexdata.FlexObject:
	return toV(value, "duration")
#






