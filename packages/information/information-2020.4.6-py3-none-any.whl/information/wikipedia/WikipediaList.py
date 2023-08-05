from .ListPage import ListPage

from internet.wikipedia import WIKIPEDIA
from pensieve import Pensieve
from chronometry.progress import ProgressBar
from silverware import Link
from pandas import DataFrame




class WikipediaList:

	@classmethod
	def of_lists(
			cls, data_type, urls, categories=None, wikipedia=None, use_cache_if_available=True,
			columns=None, representation=None, sections=None, exclude_urls=None, echo=0
	):
		"""
		:type data_type: str
		:type urls: list[str] or str
		:type categories: list[str]
		:type wikipedia: Wikipedia or NoneType
		:type columns: list[str] or NoneType or dict[str, list[str]]
		:type representation: str
		:type sections:
		:type exclude_urls: NoneType or list[str]
		:type echo: bool or int
		:rtype: WikipediaList
		"""
		exclude_urls = exclude_urls or []
		list_of_lists = cls(
			wikipedia=wikipedia, urls=urls, echo=echo, exclude_pages=exclude_urls,
			use_cache_if_available=use_cache_if_available,
			data_type='list', representation='list', sections=sections, exclude_list_pages=False
		)
		urls = [record.url for record in list_of_lists.records]
		wikipedia_list = WikipediaList(
			wikipedia=wikipedia, categories=categories, urls=urls, echo=echo,
			use_cache_if_available=use_cache_if_available,
			data_type=data_type, columns=columns, representation=representation, exclude_list_pages=True,
		)
		return wikipedia_list

	def __init__(
			self, urls, wikipedia=None, categories=None, representation=None, data_type=None,
			sections=None, columns=None, exclude_list_pages=True, echo=0,
			exclude_pages=None, use_cache_if_available=True
	):
		"""
		:param internet.wikipedia.Wikipedia wikipedia:
		:param str or list[str] urls: url of the page or list of urls of multiple pages
		:param NoneType or list[str] sections: sections of the page or None to include all sections
		:param str or list[str] data_type: could be company, brand, person, etc.
		:param str representation: either list or table
		:param NoneType or dict columns: if representation is table, it is a dictionary pointing data type to column name(s)
		"""
		self._use_cache_if_available = use_cache_if_available
		wikipedia = wikipedia or WIKIPEDIA

		if not isinstance(echo, ProgressBar):
			echo = max(0, echo)
		# error checking
		if representation is None and columns is None:
			representation = 'list'

		if representation is None:
			if columns is None or data_type is None:
				raise ValueError('both columns and data_type should be provided for unknown representation')
		elif representation == 'list':
			if data_type is None:
				raise ValueError('data_type should be provided for list representation')
		elif representation == 'table':
			if columns is None:
				raise ValueError('columns should be provided for table representation')

		self._pensieve = Pensieve()
		self.pensieve['exclude_pages'] = exclude_pages or []

		if categories is None:
			categories = []
		elif not isinstance(categories, (list, tuple)):
			categories = [categories]

		self.pensieve['categories'] = categories
		self.pensieve['urls'] = [urls] if isinstance(urls, str) else urls
		self.pensieve['sections'] = [sections] if isinstance(sections, str) else sections
		self.pensieve['data_type'] = data_type
		self.pensieve['representation'] = representation
		if isinstance(columns, dict):
			columns = {
				column_data_type: [column_names] if isinstance(column_names, str) else column_names
				for column_data_type, column_names in columns.items()
			}
		self.pensieve['columns'] = columns
		self.pensieve['exclude_list_pages'] = exclude_list_pages
		self.add_pages_and_records(wikipedia=wikipedia, echo=echo - 1)

	_STATE_ATTRIBUTES_ = ['_use_cache_if_available', '_pensieve', '_cache']

	def __getstate__(self):
		return {key: getattr(self, key) for key in self._STATE_ATTRIBUTES_}

	def __setstate__(self, state):
		for key, value in state.items():
			setattr(self, key, value)

	def __repr__(self):
		return '\n'.join([str(url) for url in self.pensieve['urls']])

	def __dir__(self):
		return list(self.pensieve.keys()) + list(super().__dir__())

	@property
	def pensieve(self):
		"""
		:rtype: Pensieve
		"""
		return self._pensieve

	@property
	def pages(self):
		"""
		:rtype: list[ListPage]
		"""
		return self.pensieve['pages']

	@property
	def records(self):
		return self.pensieve['records']

	@property
	def data(self):
		"""
		:rtype: DataFrame
		"""
		return self.pensieve['data']

	def add_pages_and_records(self, wikipedia, echo=0):
		"""
		:type wikipedia: Wikipedia
		:type echo: bool or int
		"""


		base_url = 'https://en.wikipedia.org/wiki/'
		base_length = len(base_url)

		def _get_list_pages(urls, exclude_pages, sections, data_type, representation, columns, _wikipedia, _echo=0):
			total = len(urls)

			progress_bar = ProgressBar(total=total, echo=echo)

			amount = 0
			result = []
			for url in urls:
				if _echo:
					progress_bar.show(amount=amount, text=f"{url[base_length:]}")
				result.append(ListPage(
					url=url, wikipedia=_wikipedia, sections=sections, exclude_pages=exclude_pages,
					data_type=data_type, representation=representation, columns=columns
				))
				amount += 1

			if _echo:
				progress_bar.show(amount=amount)

			return result

		self.pensieve.store(
			key='pages', precursors=['urls', 'exclude_pages', 'sections', 'data_type', 'representation', 'columns'],
			function=lambda x: _get_list_pages(
				urls=x['urls'], exclude_pages=x['exclude_pages'], sections=x['sections'], data_type=x['data_type'],
				representation=x['representation'], columns=x['columns'], _wikipedia=wikipedia, _echo=echo - 1
			),
			evaluate=False
		)

		def _get_page_records(pages, categories, exclude_list_pages):
			"""
			:type pages:
			:rtype: list[WikipediaListRecord]
			"""

			return [
				WikipediaListRecord(
					link=link, list_links=[Link(url=page.url, text=page.title)], categories=categories,
					data_type=data_type
				)
				for page in pages
				for data_type, links in page.page_links.items()
				for link in links
				if not exclude_list_pages or (
						'/wiki/list_of' not in link.url.lower() and
						'/wiki/lists_of' not in link.url.lower() and
						':' not in link.url[len('https://'):]
				)
			]

		self.pensieve.store(
			key='records', precursors=['pages', 'categories', 'exclude_list_pages'], evaluate=False,
			function=lambda x: _get_page_records(
				pages=x['pages'], categories=x['categories'],
				exclude_list_pages=x['exclude_list_pages']
			)
		)

		self.pensieve.store(
			key='data',
			precursors='records',
			function=get_records_data,
			evaluate=False
		)


class WikipediaListRecord:
	def __init__(self, data_type, categories, list_links, link, num_records=1):
		self._data_type = data_type
		self._num_records = num_records

		if isinstance(categories, (list, tuple)):
			self._categories = categories
		else:
			self._categories = [categories]

		if isinstance(list_links, (list, tuple)):
			self._list_links = list_links
		else:
			self._list_links = [list_links]

		def _remove_list_of(_link):
			text = _link.text
			list_of_str = 'list of '
			if text.lower().startswith(list_of_str):
				text = text[len(list_of_str):]
			_link._text = text.lower().replace(' ', '_').replace('\\u0026', 'and')
			return _link

		self._list_links = [_remove_list_of(x) for x in list_links]

		self._link = link

	def __getstate__(self):
		return {
			'data_type': self.data_type,
			'num_records': self._num_records,
			'categories': self.categories,
			'list_links': self.list_links,
			'link': self._link
		}

	def __setstate__(self, state):
		self._data_type = state['data_type']
		self._num_records = state['num_records']
		self._categories = state['categories']
		self._list_links = state['list_links']
		self._link = state['link']

	@property
	def dictionary(self):
		return {
			'title': self.title,
			'url': self.url,
			'data_type': self.data_type,
			'categories': self.categories,
			'list_titles': [link.text for link in self.list_links],
			'list_urls': [link.url for link in self.list_links],
			'num_records': self._num_records
		}

	def __repr__(self):
		return repr(self.dictionary)

	@property
	def data_type(self):
		return self._data_type

	def set_data_type(self, data_type):
		self._data_type = data_type

	@property
	def categories(self):
		return list(self._categories)

	@property
	def list_links(self):
		return list(self._list_links)

	@property
	def link(self):
		return self._link

	@property
	def url(self):
		return self.link.url

	@property
	def title(self):
		return self.link.text

	def __add__(self, other):
		"""
		:type other: WikipediaListRecord
		:rtype: WikipediaListRecord
		"""
		if self.data_type != other.data_type:
			raise TypeError(f'cannot merge records of two different data types: {self.data_type}, {other.data_type}')
		if self.url != other.url:
			raise TypeError(f'cannot merge records with two different urls: {self.url}, {other.url}')

		categories = []
		for x in self._categories:
			if x not in categories:
				categories.append(x)

		for y in other._categories:
			if y not in categories:
				categories.append(y)

		list_links = []
		list_urls = []
		for link in self._list_links:
			if link.url not in list_urls:
				list_links.append(link)
				list_urls.append(link.url)

		for link in other._list_links:
			if link.url not in list_urls:
				list_links.append(link)
				list_urls.append(link.url)

		return self.__class__(
			data_type=self.data_type,
			categories=categories, list_links=list_links, link=self._link,
			num_records=self._num_records + other._num_records
		)


def merge_records(lists_of_records, additional_categories=None, echo=0):
	additional_categories = additional_categories or []
	result = {}
	
	echo = max(0, echo)
	progress_bar = ProgressBar(total=len([y for x in lists_of_records for y in x]), echo=echo - 1)
	progress = 0
	for list_of_records in lists_of_records:
		for record in list_of_records:
			progress_bar.show(amount=progress, text=record.url)
			progress += 1
			if record.url not in result:
				result[record.url] = record
				new_record = record
			else:
				if result[record.url].data_type != record.data_type:
					if record.data_type in result[record.url].data_type:
						new_data_type = result[record.url].data_type
					elif result[record.url].data_type in record.data_type:
						new_data_type = record.data_type
					else:
						new_data_type = 'unknown'

					result[record.url].set_data_type(new_data_type)
					record.set_data_type(new_data_type)

				new_record = result[record.url] + record
			if len(additional_categories) > 0:
				categories = new_record.categories.copy()
				new_record._categories = list(additional_categories)
				for category in categories:
					if category not in additional_categories:
						new_record._categories.append(category)
			result[record.url] = new_record

	progress_bar.show(amount=progress, text='records merged!')
	return list(result.values())


def get_records_data(records):
	return DataFrame.from_records([r.dictionary for r in records])
