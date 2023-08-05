



import jinja2

import jk_infodatatree






def _doFormatTFmt(text:str, tfmt:str) -> str:
	if tfmt is None:
		return text
	else:
		fmtParts = tfmt.split("{}")
		if len(fmtParts) == 1:
			return fmtParts[0]
		else:
			return text.join(fmtParts)
#

def _doFormatAlert(text:str, alertState:str) -> str:
	if alertState == "crit":
		return "style=\"background-color:#800000;\"|" + text
	elif alertState == "err":
		return "style=\"background-color:#ff8000;\"|" + text
	elif alertState == "warn":
		return "style=\"background-color:#ffff00;\"|" + text
		#return "<span style=\"background-color:#808000\">" + text + "</span>"
	elif alertState is None:
		return text
	else:
		raise Exception("Unknown alert state: " + repr(alertState))
#



#
# Perform full formatting.
#
def formatValue_mediaWikiTableCell(value, dataType:str, visFlavor:str = None, alertState:str = None, tfmt:str = None) -> str:
	s = jk_infodatatree.formatValue_plaintext(value, dataType, visFlavor)
	if tfmt:
		s = _doFormatTFmt(s, tfmt)
	return _doFormatAlert(s, alertState)
#







