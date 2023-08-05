from .SpecialPage import SpecialPage

from silverware import Link
from silverware import Spoon
from ravenclaw.wrangling import standardize_columns


def get_link(link):
	if isinstance(link, Link):
		url = link.url
	elif isinstance(link, list):
		if len(link) > 0:
			link = link[0]
			if isinstance(link, Link):
				url = link.url
			else:
				return None
		else:
			return None
	elif isinstance(link, str):
		url = link
		link = Link(url=link, text='')
	else:
		return None

	if url.startswith('https://en.wikipedia.org/wiki/') and \
			'#' not in url and 'index.php?' not in url and '/wiki/file:' not in url.lower():
		return link
	else:
		return None


def get_list(base_url, sections_of_interest, first_child, exclude_pages):
	"""
	:type base_url: str
	:type sections_of_interest: Spoon
	:type first_child: bool
	:rtype: list[str]
	"""
	the_list = sections_of_interest.filter(name='li').filter(
		name='a', first_only=True, first_child=first_child, ignore_attributes={'class': 'image'}
	).find_links(base_url=base_url)
	result = [get_link(x) for x in the_list]
	return [link for link in result if link is not None and link.url not in exclude_pages]


def get_table_links(tables, columns, exclude_pages):
	result = []

	for table in tables:
		column_found = False
		for column in columns:
			if column in table.columns:
				column_found = True
				for x in table[column]:
					link = get_link(x)
					if link is not None and link not in result and link.url not in exclude_pages:
						result.append(link)
		if not column_found:
			# find similar column
			for column in columns:
				for table_column in table.columns:
					if table_column.startswith(column):
						for x in table[table_column]:
							link = get_link(x)
							if link is not None and link not in result and link.url not in exclude_pages:
								result.append(link)
						break

	return result


def get_page_lists(representation, data_type, tables, columns, base_url, sections_of_interest, exclude_pages):
	list_data = None
	table_data = None
	if representation == 'list':
		list_data = {data_type: get_list(
			base_url=base_url, sections_of_interest=sections_of_interest, first_child=True,
			exclude_pages=exclude_pages
		)}
	elif representation == 'table':
		table_data = {
			data_type: get_table_links(tables=tables, columns=column_names, exclude_pages=exclude_pages)
			for data_type, column_names in columns.items()
		}
	else:
		list_data = {data_type: get_list(
			base_url=base_url, sections_of_interest=sections_of_interest, first_child=True,
			exclude_pages=exclude_pages
		)}
		table_data = {
			data_type: get_table_links(tables=tables, columns=column_names, exclude_pages=exclude_pages)
			for data_type, column_names in columns.items()
		}
	return {'list_data': list_data, 'table_data': table_data}


def combine_list_and_table_data(list_data, table_data):
	list_data = list_data or {}
	table_data = table_data or {}

	result = {}

	for data_type in set(list_data.keys()).union(table_data.keys()):
		if data_type in list_data and data_type in table_data:
			list_links = list_data[data_type]
			table_links = table_data[data_type]
			if len(list_links) > len(table_links):
				result[data_type] = list_links
				for link in table_links:
					if link not in result[data_type]:
						result[data_type].append(link)
			else:
				result[data_type] = table_links
				for link in list_links:
					if link not in result[data_type]:
						result[data_type].append(link)
		elif data_type in list_data:
			list_links = list_data[data_type]
			result[data_type] = list_links
		else:
			table_links = table_data[data_type]
			result[data_type] = table_links
	return result


class ListPage(SpecialPage):
	def __init__(
			self, representation, columns=None, data_type=None, url=None, wikipedia=None, page=None, sections=None,
			exclude_pages=None
	):
		super().__init__(url=url, wikipedia=wikipedia, page=page, sections=sections)
		self.pensieve['exclude_pages'] = exclude_pages or []
		self.pensieve['list_representation'] = representation
		self.pensieve['list_table_columns'] = columns
		self.pensieve['list_data_type'] = data_type
		self.pensieve.store(
			key='tables',
			precursors=['sections_of_interest', 'base_url'],
			evaluate=False,
			function=lambda x: [
				standardize_columns(data=table)
				for table in Spoon.filter(
					soup=x['sections_of_interest'], name='table', attributes={'class': 'wikitable'}
				).read_tables(base_url=x['base_url'], parse_links=True)
			]
		)
		self.pensieve.store(
			key='list_and_table_links',
			precursors=[
				'list_representation', 'list_data_type', 'tables', 'list_table_columns',
				'base_url', 'sections_of_interest', 'exclude_pages'
			],
			function=lambda x: get_page_lists(
				representation=x['list_representation'],
				data_type=x['list_data_type'],
				tables=x['tables'],
				columns=x['list_table_columns'],
				base_url=x['base_url'],
				sections_of_interest=x['sections_of_interest'],
				exclude_pages=x['exclude_pages']
			)
		)
		self.pensieve.store(
			key='page_links',
			precursors='list_and_table_links',
			function=lambda x: combine_list_and_table_data(list_data=x['list_data'], table_data=x['table_data'])
		)

	@property
	def page_links(self):
		"""
		:rtype: dict[str, list[Link]]
		"""
		return self.pensieve['page_links']
