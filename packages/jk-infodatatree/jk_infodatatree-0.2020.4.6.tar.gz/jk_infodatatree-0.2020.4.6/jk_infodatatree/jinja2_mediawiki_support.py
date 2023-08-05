



import jinja2

import jk_infodatatree

from .mediawiki_support import formatValue_mediaWikiTableCell







def _jinja2AutoFormat(data, vis:str = None, tfmt:str = None) -> str:
	if isinstance(data, jinja2.runtime.Undefined):
		return "---"
	elif isinstance(data, dict):
		value = data["v"]
		dataType = data["dt"]
		alertState = data.get("a")
		return formatValue_mediaWikiTableCell(value, dataType, vis, alertState, tfmt)
	else:
		raise Exception("Unknown type: " + repr(type(data)) + " value: " + repr(data))
#

def registerJinja2Extensions_mediaWikiTableCell(env:jinja2.Environment):
	assert isinstance(env, jinja2.Environment)
	env.filters["a"] = _jinja2AutoFormat
#


