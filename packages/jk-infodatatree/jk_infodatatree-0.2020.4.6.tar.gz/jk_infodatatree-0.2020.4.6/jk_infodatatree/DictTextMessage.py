

import jk_flexdata
#import jk_json

from .DictValue import DictValue





class DictTextMessage(object):

	def __init__(self, message:str, sourceLocation:str):
		assert isinstance(message, str)
		assert message
		self.__tokens = self.__tokenize(message)

		if sourceLocation is not None:
			assert isinstance(sourceLocation, str)
			self.__sSourceLocation = ""
		else:
			self.__sSourceLocation = sourceLocation
		self.__sourceLocation = sourceLocation
	#

	def __tokenize(self, message:str):
		# tokenize the message
		tokens = []
		buffer = []
		bInVar = False
		i = 0
		while i < len(message):
			messagePart = message[i:]
			if bInVar:
				# in variable
				if messagePart.startswith("}}"):
					if buffer:
						s = "".join(buffer)

						pos = s.rfind(":")
						if pos == 0:
							raise Exception("Syntax error: " + repr(message))
						elif pos > 0:
							visFlavor = s[pos+1:]
							s = s[:pos]
						else:
							visFlavor = None

						if s.startswith("|"):
							tokens.append(("PATH", s, visFlavor))
						else:
							tokens.append(("VAR", s, visFlavor))
						buffer.clear()
					# tokens.append(("}}", None))
					i += 2
					bInVar = False
				else:
					buffer.append(message[i])
					i += 1

			else:
				# not in variable
				if messagePart.startswith("{{"):
					if buffer:
						tokens.append(("TEXT", "".join(buffer), None))
						buffer.clear()
					# tokens.append(("{{", None))
					i += 2
					bInVar = True
				else:
					buffer.append(message[i])
					i += 1

		if bInVar:
			raise Exception("Syntax error: " + repr(message))

		if buffer:
			tokens.append(("TEXT", "".join(buffer), None))
			buffer.clear()

		#jk_json.prettyPrint(tokens)
		return tokens
	#

	def format(self, dataTree:jk_flexdata.FlexObject, varValueMap:dict):
		assert isinstance(dataTree, jk_flexdata.FlexObject)

		assert isinstance(varValueMap, dict)
		for k, v in varValueMap.items():
			assert isinstance(k, str)
			assert isinstance(v, DictValue)

		# ----

		ret = []

		for tokenType, tokenText, tokenVisFlavor in self.__tokens:
			if tokenType == "TEXT":

				ret.append(tokenText)

			elif tokenType == "VAR":

				if tokenText in varValueMap:
					# value found for this variable
					v = varValueMap[tokenText]
					assert isinstance(v, DictValue)
					v = v.cloneObject()
					v.visFlavor = tokenVisFlavor
					ret.append(str(v))
				else:
					# no value found for this variable
					#print("No value found for variable: " + repr(tokenText))
					ret.append("???")

			elif tokenType == "PATH":

				_, _v = jk_flexdata.FlexDataSelector(tokenText).getOne(dataTree)
				if _v is None:
					# no value found at desired location in the path
					#print("No value found for path: " + repr(tokenText))
					ret.append("???")
				else:
					# value found at desired location in the path
					v = DictValue(_v, tokenVisFlavor, self.__sourceLocation)
					ret.append(str(v))

		return "".join(ret)
	#

#






