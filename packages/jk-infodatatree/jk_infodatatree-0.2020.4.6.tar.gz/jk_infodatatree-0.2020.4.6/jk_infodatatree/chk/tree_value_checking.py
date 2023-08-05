


import typing

import jk_flexdata
import jk_typing



from .AlertMessage import AlertMessage
from ..DictValue import DictValue
from ..DictTextMessage import DictTextMessage







class _AbstractComparator(object):

	def __init__(self, sourceLocation:str):
		if sourceLocation:
			assert isinstance(sourceLocation, str)
		else:
			sourceLocation = ""

		self.sourceLocation = sourceLocation
	#

	def check(self, dataTree:jk_flexdata.FlexObject, v:DictValue):
		raise NotImplementedError()
	#

#

class _AbstractBinaryComparator(_AbstractComparator):

	def __init__(self, refValue, refSelectorPath:str, sourceLocation:str):
		super().__init__(sourceLocation)

		if refSelectorPath:
			assert isinstance(refSelectorPath, str)
			self.refSelectorPath = jk_flexdata.FlexDataSelector(refSelectorPath)
			self.refValue = None
		else:
			self.refSelectorPath = None
			if isinstance(refValue, DictValue):
				self.refValue = refValue
			else:
				self.refValue = DictValue(refValue, None, sourceLocation)
	#

	@jk_typing.checkFunctionSignature()
	def check(self, dataTree:jk_flexdata.FlexObject, v:DictValue):
		if self.refSelectorPath is not None:
			spath, refValue = self.refSelectorPath.getOne(dataTree)
			if refValue is None:
				return -1
			else:
				refValue = DictValue(refValue, None, None)
		else:
			refValue = self.refValue

		return self._doCheck(v, refValue)
	#

	def _doCheck(self, v:DictValue, refValue:DictValue):
		raise NotImplementedError()
	#

	def __str__(self):
		if self.refSelectorPath is not None:
			s = repr(str(self.refSelectorPath))
		else:
			s = str(self.refValue)

		name = self.__class__.__name__
		p = name.rindex("_")
		name = name[p + 1:]
		name = name[0].lower() + name[1:]

		return name + " " + s
	#

#

class _Comparator_HasValues(_AbstractComparator):

	def __init__(self, sourceLocation:str):
		super().__init__(sourceLocation)
	#

	@jk_typing.checkFunctionSignature()
	def check(self, dataTree:jk_flexdata.FlexObject, v:DictValue):
		if v.test_isEmpty():
			return 0
		else:
			return 1
	#

	def __str__(self):
		return "hasValues"
	#

#

class _Comparator_GreaterThan(_AbstractBinaryComparator):

	def __init__(self, refValue, refSelectorPath:str, sourceLocation:str):
		super().__init__(refValue, refSelectorPath, sourceLocation)
	#

	@jk_typing.checkFunctionSignature()
	def _doCheck(self, v:DictValue, refValue:DictValue):
		if v.test_gt(refValue):
			return 1
		else:
			return 0
	#

#

class _Comparator_GreaterOrEqual(_AbstractBinaryComparator):

	def __init__(self, refValue, refSelectorPath:str, sourceLocation:str):
		super().__init__(refValue, refSelectorPath, sourceLocation)
	#

	@jk_typing.checkFunctionSignature()
	def _doCheck(self, v:DictValue, refValue:DictValue):
		if v.test_ge(refValue):
			return 1
		else:
			return 0
	#

#

class _Comparator_LowerThan(_AbstractBinaryComparator):

	def __init__(self, refValue, refSelectorPath:str, sourceLocation:str):
		super().__init__(refValue, refSelectorPath, sourceLocation)
	#

	@jk_typing.checkFunctionSignature()
	def _doCheck(self, v:DictValue, refValue:DictValue):
		if v.test_lt(refValue):
			return 1
		else:
			return 0
	#

#

class _Comparator_LowerOrEqual(_AbstractBinaryComparator):

	def __init__(self, refValue, refSelectorPath:str, sourceLocation:str):
		super().__init__(refValue, refSelectorPath, sourceLocation)
	#

	@jk_typing.checkFunctionSignature()
	def _doCheck(self, v:DictValue, refValue:DictValue):
		if v.test_le(refValue):
			return 1
		else:
			return 0
	#

#

class _Comparator_Equal(_AbstractBinaryComparator):

	def __init__(self, refValue, refSelectorPath:str, sourceLocation:str):
		super().__init__(refValue, refSelectorPath, sourceLocation)
	#

	@jk_typing.checkFunctionSignature()
	def _doCheck(self, v:DictValue, refValue:DictValue):
		if v.test_eq(refValue):
			return 1
		else:
			return 0
	#

#

class _Comparator_NotEqual(_AbstractBinaryComparator):

	def __init__(self, refValue, refSelectorPath:str, sourceLocation:str):
		super().__init__(refValue, refSelectorPath, sourceLocation)
	#

	@jk_typing.checkFunctionSignature()
	def _doCheck(self, v:DictValue, refValue:DictValue):
		if v.test_ne(refValue):
			return 1
		else:
			return 0
	#

#





class _RuleAction(object):

	#
	# @param		str message		The message to format later during output. Please note the special syntax that can be used to place variables within the message.
	#
	@jk_typing.checkFunctionSignature()	
	def __init__(self, comparator:_AbstractComparator, alertClass:str, message:DictTextMessage):
		self.__comparator = comparator
		self.__alertClass = alertClass
		self.__message = message
	#

	@property
	def alertClass(self) -> str:
		return self.__alertClass
	#

	#
	# Check if the condition for this action is fullfilled.
	#
	# @param	jk_flexdata.FlexObject dataTree		The full data tree to work on. This argument is required as some conditions require access to other parts of the data tree.
	# @param	DictValue v			This is the value encountered. Check /this/ value to check if action is needed.
	#
	def checkValue(self, dataTree:jk_flexdata.FlexObject, v:DictValue) -> bool:
		nCheckResult = self.__comparator.check(dataTree, v)
		if nCheckResult < 0:
			# failed for some reason
			#print("--- " + str(action.comparator) + " >>> " + jk_console.Console.ForeGround.STD_DARKYELLOW + "failed" + jk_console.Console.RESET)
			return False
		elif nCheckResult == 0:
			# no match
			#print("--- " + str(action.comparator) + " >>> " + jk_console.Console.ForeGround.STD_DARKGRAY + "no match" + jk_console.Console.RESET)
			return False
		else:
			# match!
			#print("--- " + str(action.comparator) + " >>> " + jk_console.Console.ForeGround.STD_GREEN + "MATCH!" + jk_console.Console.RESET)
			return True
	#

	def formatMessage(self, dataTree:jk_flexdata.FlexObject, varValueMap:dict):
		return self.__message.format(dataTree, varValueMap)
	#

#

class Rule(object):

	#
	# @param	str selectorPath		The string representation of the path(s) where this rule should be applied to. (required)
	# @param	str valueVisFlavor		If we need to visualize the value selected by the path use /this/ visusalization flavor. (optional)
	# @param	_RuleAction[] actions		If we have a match perform these actions. (required)
	# @param	str sourceLocation		This rule is retrieved from /this/ location. (optional)
	#
	def __init__(self, selectorPath:str, valueVisFlavor:str, actions:list, sourceLocation:str):
		assert isinstance(sourceLocation, str)
		self.__sourceLocation = sourceLocation

		if valueVisFlavor is not None:
			assert isinstance(valueVisFlavor, str)
		self.__valueVisFlavor = valueVisFlavor

		# stores a value selector: jk_flexdata.FlexDataSelector
		assert isinstance(selectorPath, str)
		self.__selector = jk_flexdata.FlexDataSelector(selectorPath)
		self.__selectorPath = selectorPath

		# stores actions: AbstractAction[]
		assert isinstance(actions, (tuple, list))
		for action in actions:
			assert isinstance(action, _RuleAction)
		self.__actions = actions
	#

	@property
	def sourceLocation(self) -> typing.Union[None,str]:
		return self.__sourceLocation
	#

	@staticmethod
	@jk_typing.checkFunctionSignature()	
	def __loadComparator(jsonData:dict, sourceLocation:str) -> _AbstractComparator:
		ruleType = jsonData["ruleType"]
		if ruleType == "hasValues":
			return _Comparator_HasValues(sourceLocation)
		elif ruleType == ">":
			return _Comparator_GreaterThan(jsonData.get("refValue"), jsonData.get("refSelector"), sourceLocation)
		elif ruleType == ">=":
			return _Comparator_GreaterOrEqual(jsonData.get("refValue"), jsonData.get("refSelector"), sourceLocation)
		elif ruleType == "<":
			return _Comparator_LowerThan(jsonData.get("refValue"), jsonData.get("refSelector"), sourceLocation)
		elif ruleType == "<=":
			return _Comparator_LowerOrEqual(jsonData.get("refValue"), jsonData.get("refSelector"), sourceLocation)
		elif ruleType == "==":
			return _Comparator_Equal(jsonData.get("refValue"), jsonData.get("refSelector"), sourceLocation)
		elif ruleType == "!=":
			return _Comparator_NotEqual(jsonData.get("refValue"), jsonData.get("refSelector"), sourceLocation)
		else:
			raise Exception("Unknown rule type specified: " + repr(ruleType) + " (" + sourceLocation + ")")
	#

	@staticmethod
	@jk_typing.checkFunctionSignature()	
	def loadFromJSON(jsonData:dict, sourceLocation:str):
		selectorPath = jsonData["selector"]
		valueVisFlavor = jsonData.get("valueVisFlavor")

		jChecks = None
		if "check" in jsonData:
			jChecks = [ jsonData["check"] ]
		elif "checks" in jsonData:
			jChecks = jsonData["checks"]
		else:
			raise Exception("No 'check' or 'checks' found! (" + sourceLocation + ")")

		actionOrActions = []
		for jCheck in jChecks:
			assert isinstance(jCheck, dict)
			visFlavors = {}
			for k, v in jCheck.items():
				if k.endswith(".visFlavor"):
					visFlavors[k[:-10]] = v
			action = _RuleAction(
				Rule.__loadComparator(jCheck, sourceLocation),
				jCheck["alert"],
				DictTextMessage(jCheck["msg"], sourceLocation),
				)
			actionOrActions.append(action)

		return Rule(selectorPath, valueVisFlavor, actionOrActions, sourceLocation)
	#

	#
	# Apply this rule. Produce output as needed.
	#
	@jk_typing.checkFunctionSignature()
	def generateAlertMessages(self, systemName:typing.Union[str,None], serviceName:typing.Union[str,None], dataTree:jk_flexdata.FlexObject):
		for spath, _vDict in self.__selector.getAll(dataTree):
			# we have a match for the current rule. now analyse if our conditions match
			# * `spath` contains the location where we found the match
			# * `:_vDict` contains the data; this is a jk_flexdata.FlexObject (if the data tree does not contain any errors)

			# let's create `v` which is a object oriented representation of that value.
			# we use DictValue as this way we have a type and formatting-aware component.
			v = DictValue(_vDict, self.__valueVisFlavor, self.__sourceLocation)

			#print("- Match: " + spath)
			for action in self.__actions:
				if not action.checkValue(dataTree, v):
					# no action required
					continue

				# produce text message

				msgArgs = {
					"value": v,
				}
				msgText = action.formatMessage(dataTree, msgArgs)

				# modify alert state of tree node

				_vDict.a = action.alertClass

				# return alert message

				yield AlertMessage(systemName, serviceName, spath, action.alertClass, msgText)

	#

#











