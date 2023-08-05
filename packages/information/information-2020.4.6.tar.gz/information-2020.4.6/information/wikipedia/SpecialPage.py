from internet.wikipedia import WikipediaPage
from copy import deepcopy
from functools import wraps
from silverware import Spoon

class SpecialPage(WikipediaPage):
	@wraps(WikipediaPage.__init__)
	def __init__(self, url, wikipedia=None, page=None, sections=None):
		if page is None:
			super().__init__(wikipedia=wikipedia, url=url)
		else:
			self._wikipedia = page.api
			self._pensieve = deepcopy(page.pensieve)
		self.pensieve['section_of_interest_names'] = sections

		def _get_sections_of_interest(body, section_of_interest_names):
			if section_of_interest_names is None:

				the_end = body.find(name='a', attrs={'href': 'http://SEEALSO'})
				if the_end is None:
					_sections = Spoon(soup=body)
				else:
					_sections = Spoon.before(element=the_end)
			else:
				try:
					_sections = Spoon.get_sections(sections=section_of_interest_names, soup=body)
				except KeyError as e:
					_sections = _get_sections_of_interest(body=body, section_of_interest_names=None)

			return _sections

		self.pensieve.store(
			key='sections_of_interest', precursors=['body', 'section_of_interest_names'],
			function=lambda x: _get_sections_of_interest(
				body=x['body'], section_of_interest_names=x['section_of_interest_names']
			),
			evaluate=False
		)
