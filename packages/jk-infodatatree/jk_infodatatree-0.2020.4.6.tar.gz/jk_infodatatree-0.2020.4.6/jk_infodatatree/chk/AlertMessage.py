


import typing

import jk_typing
import jk_flexdata




class AlertMessage(object):

	@jk_typing.checkFunctionSignature()
	def __init__(self, systemName:typing.Union[str,None], serviceName:typing.Union[str,None], locationPath:str, alertClass:str, message:str):
		self.systemName = systemName
		self.serviceName = serviceName
		self.alertClass = alertClass
		self.locationPath = locationPath
		self.message = message
	#

	def dump(self, prefix:str = None):
		if prefix is None:
			prefix = ""
		print(prefix + "Alert(" + self.alertClass + ", system=" + repr(self.systemName) + ", service=" + repr(self.serviceName) + ", loc=" + repr(self.locationPath) + ", msg=" + repr(self.message) + ")")
	#

	def toJSON(self) -> dict:
		return {
			"systemName": self.systemName,
			"serviceName": self.serviceName,
			"alertClass": self.alertClass,
			"locationPath": self.locationPath,
			"message": self.message,
		}
	#
	
	def toFlexObj(self) -> jk_flexdata.FlexObject:
		return jk_flexdata.FlexObject(self.toJSON())
	#

#






