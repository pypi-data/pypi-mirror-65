from .get_signature import get_signature
from .get_important_tokens import get_important_tokens
from .get_header_tokens import get_header_tokens
from .get_title_indicator import get_title_indicator
from .get_paragraph_statistics import get_paragraph_statistics
from .tokenize import tokenize

from pensieve import Pensieve
from internet.wikipedia import Wikipedia, Page, WIKIPEDIA

class PageSignature:
	def __init__(
			self, page=None, url=None, wikipedia=None, max_num_tokens=100, min_token_length=2,
			evaluate=True, case_sensitive=False
	):
		"""
		:type page: Page or NoneType
		:type url: str or NoneType
		:type wikipedia: Wikipedia or NoneType
		:type max_num_tokens: int
		:type min_token_length: int
		"""
		wikipedia = wikipedia or WIKIPEDIA
		self._pensieve = Pensieve()
		if page is None:
			self.pensieve['url'] = url
			self.pensieve.store(
				key='page', precursors='url', function=lambda x: wikipedia.get_page(url=x), evaluate=evaluate
			)
		else:
			self.pensieve['page'] = page

		self.pensieve['max_num_tokens'] = max_num_tokens
		self.pensieve['min_token_length'] = min_token_length

		# get required attributes
		required_attributes = ['headers', 'title', 'categories', 'info_box', 'summary', 'paragraphs', 'paragraph_links']
		for key in required_attributes:
			self.pensieve.store(key=key, precursors='page', function=lambda x: x[key], evaluate=evaluate)

		self.pensieve.store(key='title_indicator', precursors='title', function=get_title_indicator)
		self.pensieve.store(
			key='paragraph_tokens', precursors='paragraphs', evaluate=evaluate,
			function=lambda x: [tokenize(paragraph.text.lower()) for paragraph in x]
		)

		self.pensieve.store(
			key='paragraph_statistics', precursors=['paragraph_links', 'paragraph_tokens'],
			function=lambda x: get_paragraph_statistics(
				paragraph_links=x['paragraph_links'], paragraph_tokens=x['paragraph_tokens']
			),
			evaluate=evaluate
		)

		self.pensieve.store(
			key='important_tokens', precursors=['paragraph_tokens', 'max_num_tokens', 'min_token_length'],
			function=lambda x: get_important_tokens(
				paragraph_tokens=x['paragraph_tokens'],
				num_tokens=x['max_num_tokens'], min_length=x['min_token_length']),
			evaluate = False
		)

		self.pensieve.store(
			key='header_tokens', precursors=['headers'], evaluate=evaluate,
			function=get_header_tokens
		)

		self.pensieve.store(
			key='summary_tokens', precursors=['summary'], evaluate=evaluate, materialize=False,
			function=tokenize
		)

		self.pensieve.store(
			key='signature',
			precursors=[
				'title_indicator', 'categories', 'info_box', 'important_tokens',
				'header_tokens', 'paragraph_statistics', 'summary_tokens'
			],
			evaluate=evaluate,
			function=lambda x: get_signature(
				title_indicator=x['title_indicator'],
				tokens=x['important_tokens'], info_box=x['info_box'], categories=x['categories'],
				header_tokens=x['header_tokens'], paragraph_statistics=x['paragraph_statistics'],
				summary_tokens=x['summary_tokens'], case_sensitive=case_sensitive
			)
		)

	@property
	def signature(self):
		"""
		:rtype: dict
		"""
		return self.pensieve['signature']

	@property
	def pensieve(self):
		"""
		:rtype: Pensieve
		"""
		return self._pensieve


def get_page_signature(url=None, page=None, wikipedia=None, max_num_tokens=100, min_token_length=2):
	signature = PageSignature(
		page=page, url=url, wikipedia=wikipedia, max_num_tokens=max_num_tokens, min_token_length=min_token_length
	)
	return signature.signature
