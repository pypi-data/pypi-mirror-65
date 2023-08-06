from collections import Counter
from linguistics.english import get_stop_words

_NONPRONOUN_SW = get_stop_words(include_pronoun_forms=False)


def get_signature(
		title_indicator, header_tokens, tokens, info_box, categories, paragraph_statistics,
		summary_tokens, case_sensitive=False
):

	if title_indicator is None:
		title_indicator_list = ['title_indicator:none']
	else:
		title_indicator_list = [f'title_indicator:{title_indicator.lower()}']

	lowercase_header_tokens = [str(header_token).lower() for header_token in header_tokens]
	header_token_list = [f'header_token:{header_token}' for header_token in lowercase_header_tokens]

	lowercase_tokens = [str(token).lower() for token in tokens]
	token_list = [f'token:{token}' for token in lowercase_tokens if token not in _NONPRONOUN_SW]

	lowercase_info_list = [str(info).lower() for info in info_box.keys()]
	info_list = [
		f'info:{info}' for info in lowercase_info_list
		if info not in _NONPRONOUN_SW and not info.startswith('unknown_row_')
	]

	lowercase_category_list = [str(category).lower() for category in categories]
	category_list = [f'category:{category}' for category in lowercase_category_list if category not in _NONPRONOUN_SW]

	summary_list = [f'summary:{token}' for token in summary_tokens if token not in _NONPRONOUN_SW]

	signature = title_indicator_list + header_token_list + token_list + info_list + category_list + summary_list
	if not case_sensitive:
		signature = [x.lower() for x in signature]

	result = dict(Counter(signature))
	result.update(paragraph_statistics)
	return result
