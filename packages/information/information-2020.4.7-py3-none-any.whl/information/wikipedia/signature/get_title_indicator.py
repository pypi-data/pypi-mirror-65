def get_title_indicator(s):
	open_bracket = s.find('(')
	close_bracket = s.find(')')
	if open_bracket >= 0 and close_bracket >= 0 and open_bracket < close_bracket:
		return s[s.find("(") + 1:s.find(")")]
	else:
		return None
