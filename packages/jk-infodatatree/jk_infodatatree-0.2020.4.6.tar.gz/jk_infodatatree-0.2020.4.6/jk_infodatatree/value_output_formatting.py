



import datetime
import time

import jk_utils





################################################################################################################################
#### Data converters
################################################################################################################################




def _doFormatSecsDiff(v:float) -> str:
	nTotalSeconds = int(round(v))
	nAbsTotalSeconds = abs(nTotalSeconds)
	s = "+" if nTotalSeconds >= 0 else "-"
	return s + jk_utils.formatTime(nAbsTotalSeconds)
#

def _doFormatTempC(v:float) -> str:
	return str(round(v, 1)) + " °C"
#

def _doFormatFrequency(v:float) -> str:
	if v < 0:
		return "- Hz"
	v = int(v)
	if v > 1000:
		# kHz
		if v > 1000:
			# MHz
			if v > 1000000:
				# GHz
				return str(round(v / 1000000000, 2)) + " GHz"
			else:
				# < 1 GHz
				return str(round(v / 1000000, 2)) + " MHz"
		else:
			# < 1 MHz
			return str(round(v / 1000, 2)) + " kHz"
	else:
		# < 1 kHz
		return str(v) + " Hz"
#

def _formatBytes(v:float) -> str:
	if v < 0:
		return "---"
	s = jk_utils.formatBytes(v)
	return s[:-1] + " " + s[-1] + "B"
#

def _formatDurationSecondsHR(v:float) -> str:
	if v < 0:
		return "---"
	t = int(round(v))
	if t == 1:
		return "1 second"
	else:
		return str(t) + " seconds"
#

def _formatDurationHR(v:float) -> str:
	if v < 0:
		return "---"

	nTimeDelta = v

	n = nTimeDelta
	nDays = int(n / (3600*24))
	n = n - nDays * 3600*24
	nHours = int(n / 3600)
	n = n - nHours * 3600
	nMinutes = int(n / 60)
	nSeconds = int(round(n - nMinutes * 60))

	bIgnoreMinutes = False
	bIgnoreSeconds = False
	if nTimeDelta > 3600*24:
		bIgnoreMinutes = True
		bIgnoreSeconds = True
	elif nTimeDelta > 3600:
		bIgnoreSeconds = True

	ret = []
	if nDays:
		ret.append(str(nDays) + " " + ("day" if nDays == 1 else "days"))
	if nHours:
		ret.append(str(nHours) + " " + ("hour" if nHours == 1 else "hours"))
	if nMinutes and not bIgnoreMinutes:
		ret.append(str(nMinutes) + " " + ("minutes" if nMinutes == 1 else "minutes"))
	if nSeconds and not bIgnoreSeconds:
		ret.append(str(nSeconds) + " " + ("second" if nSeconds == 1 else "seconds"))
	return ", ".join(ret)
#

def _formatTimeStampEU(t:float) -> str:
	if t < 0:
		return "---"

	dt = datetime.datetime.fromtimestamp(t)

	sDate = dt.strftime("%d.%M.%Y")
	sTime = dt.strftime("%H:%m:%S")

	return sDate + " " + sTime
#

def _formatTimeStampPastHR(t:float) -> str:
	if t < 0:
		return "---"

	dt = datetime.datetime.fromtimestamp(t)
	nYear = dt.year
	nMonth = dt.month
	nDay = dt.day

	tNow = datetime.datetime.now()
	if dt > tNow:
		# specified timestamp is from the future
		return "---"

	nSecondsToday = tNow.hour * 3600 + tNow.minute * 60 + tNow.second
	nDaysAgo = int(((tNow - dt).total_seconds() + 1 - nSecondsToday) / (24*3600))

	if nDaysAgo > 7:
		sDate = dt.strftime("%-dth of %B")
	elif nDaysAgo == 0:
		sDate = "today"
	elif nDaysAgo == 1:
		sDate = "yesterday"
	else:
		return str(nDaysAgo) + " days ago"

	sTime = dt.strftime("%H:%m:%S")

	return sDate + " " + sTime
#

def _doFormatBool(v:bool) -> str:
	return "yes" if v else "no"
#

def _doFormatInt(v:int) -> str:
	return str(v)
#

def _doFormatFloatPercent0(v:float) -> str:
	v = v * 100
	return str(round(v)) + "%"
#

def _doFormatFloatPercent1(v:float) -> str:
	v = v * 100
	return str(round(v, 1)) + "%"
#

def _doFormatFloatPercent2(v:float) -> str:
	v = v * 100
	return str(round(v, 2)) + "%"
#

def _doFormatFloat(v:float) -> str:
	return str(v)
#

def _doFormatStr(v:str) -> str:
	return v
#

def _formatStrList(data:list) -> str:
	return ", ".join(data)
#

def _formatSortedStrList(data:list) -> str:
	return ", ".join(sorted(data))
#

def _formatShortenedStrList(data:list) -> str:
	d = data[:3]
	s = ", ".join(sorted(d))
	if len(data) > 3:
		s += ", ..."
	return s
#

def _formatIntList(data:list) -> str:
	return ", ".join([ str(x) for x in data ])
#

def _formatSortedIntList(data:list) -> str:
	return ", ".join([ str(x) for x in sorted(data) ])
#

def _formatShortenedIntList(data:list) -> str:
	d = data[:3]
	d = [ str(x) for x in d ]
	s = ", ".join(d)
	if len(data) > 3:
		s += ", ..."
	return s
#

def _formatFloatList(data:list) -> str:
	return ", ".join([ str(x) for x in data ])
#

def _formatSortedFloatList(data:list) -> str:
	return ", ".join([ str(x) for x in sorted(data) ])
#

def _formatShortenedFloatList(data:list) -> str:
	d = data[:3]
	d = [ str(x) for x in d ]
	s = ", ".join(d)
	if len(data) > 3:
		s += ", ..."
	return s
#




################################################################################################################################
#### Data structure that contains all definitions, descriptions and converters to call
################################################################################################################################




DEFINITIONS = {
	"bool": {
		"description": {
			"valueDataType": "bool",
			"text": "Boolean value",
		},
		"pyDataType": bool,
		"notDataType": ( int, float ),
		"default": {
			"callable": _doFormatBool,
			"text": "Outputs 'yes' or 'no'",
			"outputExample": "yes",
		},
		"visFlavors": {
		}
	},
	"int": {
		"description": {
			"valueDataType": "int",
			"text": "Integer value",
		},
		"pyDataType": int,
		"notDataType": ( bool, float ),
		"default": {
			"callable": _doFormatInt,
			"text": "The input value as provided",
			"outputExample": "123",
		},
		"visFlavors": {
		}
	},
	"float": {
		"description": {
			"valueDataType": "float",
			"text": "Float value",
		},
		"pyDataType": float,
		"notDataType": ( int, bool ),
		"default": {
			"callable": _doFormatFloat,
			"text": "The input value as provided",
			"outputExample": "3.1415927",
		},
		"visFlavors": {
			"%0": {
				"callable": _doFormatFloatPercent0,
				"text": "The float value formatted as a percent value with zero decimal digits",
				"outputExample": "23%",
			},
			"%1": {
				"callable": _doFormatFloatPercent1,
				"text": "The float value formatted as a percent value with one decimal digit",
				"outputExample": "23.4%",
			},
			"%2": {
				"callable": _doFormatFloatPercent2,
				"text": "The float value formatted as a percent value with two decimal digits",
				"outputExample": "23.45%",
			},
		}
	},
	"str": {
		"description": {
			"valueDataType": "str",
			"text": "String value",
		},
		"pyDataType": str,
		"default": {
			"callable": _doFormatStr,
			"text": "The input string as provided",
			"outputExample": "abcdef",
		},
		"visFlavors": {
		}
	},

	"secsdiff": {
		"description": {
			"valueDataType": "int, float",
			"constraint": ">= 0",
			"text": "Number of seconds",
		},
		"pyDataType": ( int, float ),
		"default": {
			"callable": _doFormatSecsDiff,
			"text": "The difference in time",
			"outputExample": "+00:02:39",
		},
		"visFlavors": {
		}
	},
	"tempc": {
		"description": {
			"valueDataType": "int, float",
			"text": "Temperature in °C",
		},
		"pyDataType": ( int, float ),
		"default": {
			"callable": _doFormatTempC,
			"text": "The temperature value in human readable form",
			"outputExample": "37.1 °C",
		},
		"visFlavors": {
		}
	},
	"freq": {
		"description": {
			"valueDataType": "int, float",
			"constraint": ">= 0",
			"text": "Frequency = Number of events per second",
		},
		"pyDataType": ( int, float ),
		"default": {
			"callable": _doFormatFrequency,
			"text": "The frequency in human readable form",
			"outputExample": "3.45 GHz",
		},
		"visFlavors": {
		}
	},
	"bytes": {
		"description": {
			"valueDataType": "int",
			"constraint": ">= 0",
			"text": "Number of bytes",
		},
		"pyDataType": int,
		"default": {
			"callable": _formatBytes,
			"text": "The number of bytes in human readable form",
			"outputExample": "3.45 MB",
		},
		"visFlavors": {
		}
	},
	"timestamp": {
		"description": {
			"valueDataType": "int, float",
			"constraint": "> 0",
			"text": "Number of seconds since Epoch",
		},
		"pyDataType": ( int, float ),
		"default": {
			"callable": _formatTimeStampEU,
			"text": "Returns time stamp in human readable form",
			"outputExample": "23.03.2020 12:03:59",
		},
		"visFlavors": {
			"age": {
				"callable": _formatTimeStampPastHR,
				"text": "Returns time stamp in human readable form",
				"outputExample": "yesterday 12:03:59",
			},
		}
	},
	"timestamputc": {
		"description": {
			"valueDataType": "int, float",
			"constraint": "> 0",
			"text": "Number of UTC seconds since Epoch",
		},
		"pyDataType": ( int, float ),
		"default": {
			"callable": _formatTimeStampEU,
			"text": "Returns time stamp in human readable form",
			"outputExample": "23.03.2020 12:03:59",
		},
		"visFlavors": {
			"age": {
				"callable": _formatTimeStampPastHR,
				"text": "Returns time stamp in human readable form",
				"outputExample": "yesterday 12:03:59",
			},
		}
	},
	"duration": {
		"description": {
			"valueDataType": "int, float",
			"constraint": ">= 0",
			"text": "Number of seconds",
		},
		"pyDataType": ( int, float ),
		"default": {
			"callable": _formatDurationHR,
			"text": "Time spent in human readable form",
			"outputExample": "3 hours, 1 minute, 29 seconds",
		},
		"visFlavors": {
			"secs": {
				"callable": _formatDurationSecondsHR,
				"text": "Number of seconds spent in human readable form",
				"outputExample": "129 seconds",
			},
		}
	},

	"str[]": {
		"description": {
			"valueDataType": "str[]",
			"text": "List of string values",
		},
		"pyDataType": ( tuple, list ),
		"pySubDataType": str,
		"default": {
			"callable": _formatStrList,
			"text": "String values separated by comma",
			"outputExample": "Mon, Tue, Wed, Thur, Fri",
		},
		"visFlavors": {
			"sorted": {
				"callable": _formatSortedStrList,
				"text": "Sorted string values separated by comma",
				"outputExample": "Mon, Tue, Wed, Thur, Fri",
			},
			"shorten": {
				"callable": _formatShortenedStrList,
				"text": "Shortened string value list separated by comma",
				"outputExample": "Mon, Tue, Wed, ...",
			},
		},
	},
	"int[]": {
		"description": {
			"valueDataType": "int[]",
			"text": "List of integer values",
		},
		"pyDataType": ( tuple, list ),
		"pySubDataType": int,
		"default": {
			"callable": _formatIntList,
			"text": "Integer values separated by comma",
			"outputExample": "99, 4, 87, 7",
		},
		"visFlavors": {
			"sorted": {
				"callable": _formatSortedIntList,
				"text": "Sorted integer values separated by comma",
				"outputExample": "4, 7, 87, 99",
			},
			"shorten": {
				"callable": _formatShortenedStrList,
				"text": "Shortened integer value list separated by comma",
				"outputExample": "99, 4, 87, ...",
			},
		},
	},
	"float[]": {
		"description": {
			"valueDataType": "float[]",
			"text": "List of float values",
		},
		"pyDataType": ( tuple, list ),
		"pySubDataType": float,
		"default": {
			"callable": _formatFloatList,
			"text": "Float values separated by comma",
			"outputExample": "99.9, 4.1, 87, 7.358",
		},
		"visFlavors": {
			"sorted": {
				"callable": _formatSortedFloatList,
				"text": "Sorted float values separated by comma",
				"outputExample": "4.1, 7.358, 87, 99.9",
			},
			"shorten": {
				"callable": _formatShortenedStrList,
				"text": "Shortened float value list separated by comma",
				"outputExample": "99.9, 4.1, 87, ...",
			},
		},
	},
}

ALL_VALID_DATA_TYPES = list(DEFINITIONS.keys())

ALIASES = {
	"uptime": {
		"valueDataType": "duration",
		"visFlavor": None,
	},
	"age": {
		"valueDataType": "duration",
		"visFlavor": None,
	},
}




################################################################################################################################
#### Main functions
################################################################################################################################




#
# Core formatting subroutine.
#
def formatValue_plaintext(value, dataType:str, visFlavor:str = None) -> str:
	if value is None:
		return "---"
	assert dataType is not None

	aliasStruct = ALIASES.get(dataType)
	if aliasStruct is not None:
		dataType = aliasStruct["valueDataType"]
		_visFlavors = aliasStruct.get("aliasStruct", visFlavor)
		visFlavor = visFlavor if None else _visFlavors

	dataStruct = DEFINITIONS[dataType]

	# check types

	if not isinstance(value, dataStruct["pyDataType"]):
		raise Exception("Expected value of type " + dataStruct["description"]["valueDataType"] + " but data value is of non-suitable python type " + repr(type(value)))
	if "pySubDataType" in dataStruct:
		pySubDataType = dataStruct["pySubDataType"]
		for item in value:
			if not isinstance(item, pySubDataType):
				raise Exception("Expected value of type " + dataStruct["description"]["valueDataType"] + " but item value is of non-suitable python type " + repr(type(item)))

	# convert

	if visFlavor is None:
		return dataStruct["default"]["callable"](value)
	else:
		if visFlavor in dataStruct["visFlavors"]:
			return dataStruct["visFlavors"][visFlavor]["callable"](value)
		else:
			raise Exception("For value of type " + dataStruct["description"]["valueDataType"] + " this visFlavor value is invalid: " + repr(visFlavor))
#





def generateValueDataTypeDocu() -> str:
	outputLines = []

	for key in sorted(DEFINITIONS.keys()):
		dataStruct = DEFINITIONS[key]

		outputLines.append("# Data types")
		outputLines.append("")
		outputLines.append("The following sections provide an overview about all data types supported by the data value data structure.")
		outputLines.append("")
		outputLines.append("## Data type: '" + key + "'")
		outputLines.append("")
		outputLines.append("General information:")
		outputLines.append("")
		outputLines.append("* *FlexStruct type name:* `" + key + "`")
		outputLines.append("* *Input value:* " + dataStruct["description"]["text"])
		outputLines.append("* *Expected value type:* `" + dataStruct["description"]["valueDataType"] + "`")
		outputLines.append("")
		outputLines.append("Default output:")
		outputLines.append("")
		outputLines.append("* *Description:* " + dataStruct["default"]["text"])
		outputLines.append("* *Output example:* \"`" + dataStruct["default"]["outputExample"] + "`\"")
		outputLines.append("")
		if ("visFlavors" in dataStruct) and dataStruct["visFlavors"]:
			outputLines.append("The following visualization flavors exist:")
			outputLines.append("")
			for visFlavorName in dataStruct["visFlavors"]:
				d = dataStruct["visFlavors"][visFlavorName]
				outputLines.append("* \"`" + visFlavorName + "`\"")
				outputLines.append("\t* *Description:* " + d["text"])
				outputLines.append("\t* *Output example:* \"`" + d["outputExample"] + "`\"")
		else:
			outputLines.append("There are no visualization flavors for this data type.")
		outputLines.append("")

	return "\n".join(outputLines)
#


