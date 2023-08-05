from .tokenize import tokenize


def get_header_tokens(headers):
	tokens = []
	for header in headers:
		text = header.text
		if text == 'SEEALSO':
			break
		text = text[:-6] if text.endswith('[edit]') else text
		tokens += tokenize(text)
	return tokens