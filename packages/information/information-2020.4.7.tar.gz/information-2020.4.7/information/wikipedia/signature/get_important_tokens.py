def get_important_tokens(paragraph_tokens, num_tokens, min_length):
	"""
	:param paragraphs soup: list[Tag]
	:param int num_tokens: number of tokens required to finish the job
	:param int min_length: minimum length for a token to be considered (anything shorter will be ignored)
	:rtype: list[str]
	"""
	important_tokens = []
	for tokens in paragraph_tokens:
		if len(important_tokens) >= num_tokens:
			break
		important_tokens += [token for token in tokens if len(token) >= min_length]
	return important_tokens
