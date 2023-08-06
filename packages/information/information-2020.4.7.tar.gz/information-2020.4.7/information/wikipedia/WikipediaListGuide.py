from .WikipediaList import WikipediaList


class WikipediaListGuide:
	def __init__(
			self, list_type, data_type, urls, categories, wikipedia,
			echo, representation=None,
			use_cache_if_available=True, exclude_urls=None, columns=None, sections=None,
			exclude_pages=None, exclude_list_pages=None
	):
		"""
		:type list_type: str
		:type data_type: str
		:type urls: str or list[str]
		:type categories: list[str]
		:type wikipedia: Wikipedia
		:type echo: NoneType or int or ProgressBar
		:type representation: str or NoneType
		:type use_cache_if_available: bool
		:type exclude_urls: NoneType or list[str]
		:type columns: dict[str, list] or dict[str, str]
		:type sections: list[str]
		:type exclude_pages: NoneType or list[str]
		:type exclude_list_pages: NoneType or list[str]
		"""
		self.list_type = list_type
		self.data_type = data_type
		self.urls = urls
		self.categories = categories
		self.wikipedia = wikipedia
		self.columns = columns
		self.representation = representation
		self.sections = sections
		self.exclude_urls = exclude_urls
		self.exclude_list_pages = exclude_list_pages
		self.exclude_pages = exclude_pages
		self.use_cache_if_available = use_cache_if_available
		self.echo = echo

	def get_list(self):
		if self.list_type == 'list_of_lists' or self.list_type == 'list_of_list':
			return WikipediaList.of_lists(
				data_type=self.data_type, urls=self.urls, categories=self.categories,
				wikipedia=self.wikipedia, columns=self.columns, representation=self.representation,
				sections=self.sections, exclude_urls=self.exclude_urls, echo=self.echo
			)
		elif self.list_type == 'list':
			return WikipediaList(
				urls=self.urls, wikipedia=self.wikipedia, categories=self.categories,
				representation=self.representation, data_type=self.data_type, sections=self.sections,
				columns=self.columns, exclude_list_pages=self.exclude_list_pages, exclude_pages=self.exclude_pages,
				use_cache_if_available=self.use_cache_if_available, echo=self.echo
			)