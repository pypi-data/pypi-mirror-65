from .SpecialPage import SpecialPage

from silverware import Link
import pandas as pd


class IosDevices(SpecialPage):
	def __init__(self, wikipedia=None, page=None):
		super().__init__(wikipedia=wikipedia, url='https://en.wikipedia.org/wiki/List_of_iOS_devices', page=page)
		self._load_extra_stuff()

	def _load_extra_stuff(self):
		def get_main_tables(x):
			result = []
			for table in x:
				if 'announced' in table.columns and 'released' in table.columns:
					result.append(table)
			return pd.concat(result).reset_index(drop=True)

		self.pensieve.store(
			key='ios_device_table', precursors='tables', function=get_main_tables,
			evaluate=False
		)

		def get_page_urls(x):
			result = []
			for link in list(x['model']):
				if isinstance(link, Link):
					if link.url.startswith('https://en.wikipedia.org/wiki/'):
						if link.url not in result:
							result.append(link.url)
			return result

		self.pensieve.store(
			key='ios_device_page_urls', precursors='ios_device_table', function=get_page_urls,
			evaluate=False
		)
