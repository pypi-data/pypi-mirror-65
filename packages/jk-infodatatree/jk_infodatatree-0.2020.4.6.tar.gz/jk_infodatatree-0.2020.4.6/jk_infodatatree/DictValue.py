



import jk_flexdata

from .value_output_formatting import formatValue_plaintext









class DictValue(object):

	def __init__(self, v, visFlavor:str, sourceLocation:str, _clone:tuple = None):
		if _clone is not None:
			self.v, self.dt, self.visFlavor, self.sourceLocation = _clone
			return

		if visFlavor is not None:
			assert isinstance(visFlavor, str)

		if sourceLocation is not None:
			assert isinstance(sourceLocation, str)
			sSourceLocation = sourceLocation
		else:
			sSourceLocation = ""

		if v is None:
			self.dt = None
			self.v = None
		elif isinstance(v, dict):
			self.dt = v["dt"]
			self.v = v["v"]
		elif isinstance(v, jk_flexdata.FlexObject):
			self.dt = v.dt
			self.v = v.v
		elif isinstance(v, bool):
			self.dt = "bool"
			self.v = v
		elif isinstance(v, float):
			self.dt = "float"
			self.v = v
		elif isinstance(v, int):
			self.dt = "int"
			self.v = v
		elif isinstance(v, str):
			self.dt = "str"
			self.v = v
		elif isinstance(v, list):
			self.dt = "str[]"
			self.v = v
			for item in v:
				if isinstance(item, float):
					self.dt = "float[]"
					self.v = v
					break
				elif isinstance(item, int):
					self.dt = "int[]"
					self.v = v
					break
				elif isinstance(item, str):
					self.dt = "str[]"
					self.v = v
					break
				else:
					raise Exception("Unexpected list item data type: " + str(type(item)) + " (" + sSourceLocation + ")")
		else:
			raise Exception("Unexpected data type: " + str(type(v)) + " (" + sSourceLocation + ")")

		self.visFlavor = visFlavor

		self.sourceLocation = sourceLocation
	#

	def toJSON(self) -> dict:
		return {
			"v": self.v,
			"dt": self.dt
		}
	#

	def dump(self):
		print("DictValue(")
		print("\tdt = " + repr(self.dt))
		print("\tv = " + repr(self.v))
		print("\tvisFlavor = " + repr(self.visFlavor))
		print("\tsourceLocation = " + repr(self.sourceLocation))
		print(")")
	#

	def __str__(self):
		if self.dt is None:
			return "---"
		else:
			return formatValue_plaintext(self.v, self.dt, self.visFlavor)
	#

	def test_eq(self, other):
		assert isinstance(other, DictValue)

		if other.dt != self.dt:
			return False
		return other.v == self.v
	#

	def test_ne(self, other):
		assert isinstance(other, DictValue)

		if other.dt != self.dt:
			return True
		return other.v != self.v
	#

	def test_ge(self, other):
		assert isinstance(other, DictValue)

		if isinstance(other.v, (int, float)) and isinstance(self.v, (int, float)):
			return self.v >= other.v
		return False
	#

	def test_gt(self, other):
		assert isinstance(other, DictValue)

		if isinstance(other.v, (int, float)) and isinstance(self.v, (int, float)):
			return self.v > other.v
		return False
	#

	def test_le(self, other):
		assert isinstance(other, DictValue)

		if isinstance(other.v, (int, float)) and isinstance(self.v, (int, float)):
			return self.v <= other.v
		return False
	#

	def test_lt(self, other):
		assert isinstance(other, DictValue)

		if isinstance(other.v, (int, float)) and isinstance(self.v, (int, float)):
			return self.v < other.v
		return False
	#

	def test_isEmpty(self):
		if isinstance(self.v, (str, list)):
			return len(self.v) == 0
		return False
	#

	def cloneObject(self):
		return DictValue(None, None, None, _clone=(self.v, self.dt, self.visFlavor, self.sourceLocation))
	#

#




















