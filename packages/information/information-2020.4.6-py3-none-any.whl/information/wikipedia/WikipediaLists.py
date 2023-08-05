from .WikipediaList import WikipediaList, merge_records, get_records_data
from .WikipediaListGuide import WikipediaListGuide
from pensieve import Pensieve
from pandas import DataFrame
from chronometry.progress import ProgressBar


class WikipediaLists:
	def __init__(self, wikipedia_lists, categories=None, echo=0):
		"""
		:type wikipedia_lists: dict[str, WikipediaList] or dict[str, WikipediaListGuide
		"""
		if not isinstance(wikipedia_lists, dict):
			raise TypeError('wikipedia_lists should be a dictionary')

		echo = max(0, echo)
		progress_bar = ProgressBar(total=len(wikipedia_lists), echo=echo - 1)
		progress_amount = 0
		the_list = []
		for key, value in wikipedia_lists.items():
			progress_bar.show(amount=progress_amount, text=key)
			if isinstance(value, WikipediaListGuide):
				the_list.append(value.get_list())
			else:
				the_list.append(value)
			progress_amount += 1

		progress_bar.show(amount=progress_amount, text='adding lists complete!')


		if categories is None:
			categories = []
		elif not isinstance(categories, (list, tuple)):
			categories = [categories]

		self._pensieve = Pensieve()
		self.pensieve['categories'] = categories
		self.pensieve['sublists'] = the_list

		self.pensieve.store(
			key='records', precursors=['sublists', 'categories'],
			function=lambda x: merge_records(
				lists_of_records=[y.records for y in x['sublists']], additional_categories=x['categories'],
				echo=echo
			),
			evaluate=False
		)

		self.pensieve.store(
			key='data',
			precursors='records',
			function=get_records_data,
			evaluate=False
		)

	_STATE_ATTRIBUTES_ = ['_pensieve']

	def __getstate__(self):
		return {key: getattr(self, key) for key in self._STATE_ATTRIBUTES_}

	def __setstate__(self, state):
		for key, value in state.items():
			setattr(self, key, value)

	def __repr__(self):
		return '\n'.join([repr(x) for x in self.pensieve['sublists']])

	@property
	def pensieve(self):
		"""
		:rtype: Pensieve
		"""
		return self._pensieve

	@property
	def lists(self):
		"""
		:rtype: list[WikipediaList]
		"""
		return self.pensieve['sublists']

	@property
	def records(self):
		"""
		:rtype: list[dict[str]]
		"""
		return self.pensieve['records']

	@property
	def data(self):
		"""
		:rtype: DataFrame
		"""
		return self.pensieve['data']
