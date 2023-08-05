
def get_paragraph_statistics(paragraph_tokens, paragraph_links):
	all_tokens = []
	all_links = []
	for tokens in paragraph_tokens:
		all_tokens += tokens

	for links in paragraph_links:
		all_links += links

	num_tokens = len(all_tokens)
	num_links = len(all_links)
	num_unique_tokens = len(set(all_tokens))
	num_unique_links = len(set(all_links))

	return {
		'num_tokens': num_tokens, 'num_links': num_links,
		'num_unique_tokens': num_unique_tokens, 'num_unique_links': num_unique_links,
		'links_to_tokens_ratio': num_links / num_tokens if num_tokens != 0 else -1,
		'unique_links_to_tokens_ratio': num_unique_links / num_tokens if num_tokens != 0 else -1,
		'unique_tokens_ratio': num_unique_tokens / num_tokens if num_tokens != 0 else 1
	}
