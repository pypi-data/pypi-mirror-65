




from jk_flexdata import FlexObject, NONE

from .value_output_formatting import ALL_VALID_DATA_TYPES







def _verifyFlexTreeStruct(pathParts:list, data):
	if data is None or data is NONE:
		return

	elif isinstance(data, FlexObject):
		if "dt" in data:
			# data node
			if data["dt"] not in ALL_VALID_DATA_TYPES:
				raise Exception("|" + "|".join(pathParts))

		else:
			# descend
			for k in data:
				v = data[k]
				pathParts.append(k)
				_verifyFlexTreeStruct(pathParts, v)
				del pathParts[-1]

	elif isinstance(data, (tuple, list)):
		# descend
		n = 0
		for v in data:
			pathParts.append(str(n))
			_verifyFlexTreeStruct(pathParts, v)
			del pathParts[-1]
			n += 1

	else:
		raise Exception("|" + "|".join(pathParts))
#




def verifyFlexTreeStruct(data:FlexObject):
	if data is None or data is NONE:
		raise Exception("Value is (null)!")

	assert isinstance(data, FlexObject)

	_verifyFlexTreeStruct([], data)
#









