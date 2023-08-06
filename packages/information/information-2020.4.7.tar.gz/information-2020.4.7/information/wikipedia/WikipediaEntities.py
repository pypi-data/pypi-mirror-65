from .lists.political_entities import get_political_entities
from .lists.space_objects import get_space_objects
from .lists.brands import get_brands
from .lists.companies import get_companies
from .lists.concepts import get_concepts
from .lists.diseases import get_diseases
from .lists.fictional_characters import get_fictional_characters
from .lists.geographical_features import get_geographical_features
from .lists.historic_events import get_historic_events
from .lists.landmarks import get_landmarks
from .lists.music_bands import get_music_bands
from .lists.organizations import get_organizations
from .lists.persons import get_persons
from .lists.products import get_products
from .lists.species import get_species, get_breeds
from .lists.supernatural_beings import get_supernatural_beings
from .lists.vehicles import get_vehicles
from .lists.weapons import get_weapons

from .signature.PageSignature import PageSignature

from disk import Cache
from chronometry.progress import ProgressBar, iterate
from pandas import concat
from math import ceil
from pensieve import Pensieve
from joblib import delayed, Parallel


LIST_FUNCTIONS = {
	'brand': get_brands,
	'company': get_companies,
	'concept': get_concepts,
	'disease': get_diseases,
	'fictional_character': get_fictional_characters,
	'geographical_feature': get_geographical_features,
	'historic_event': get_historic_events,
	'landmark': get_landmarks,
	'artist_or_band': get_music_bands,
	'organization': get_organizations,
	'person': get_persons,
	'political_entity': get_political_entities,
	'product': get_products,
	'space_object': get_space_objects,
	'specie': get_species,
	'breed': get_breeds,
	'supernatural_being': get_supernatural_beings,
	'vehicle': get_vehicles,
	'weapon': get_weapons
}


def get_data(entity_type, wikipedia, echo):
	wikipedia_list = LIST_FUNCTIONS[entity_type](wikipedia=wikipedia, echo=echo)
	return wikipedia_list.data

KEYS = sorted(LIST_FUNCTIONS.keys())


class WikipediaEntities:
	def __init__(
			self, sample_size=10000, different_type_ratio=1 / 10,
			wikipedia=None, num_threads=-1,
			echo=3, cache=None, random_state=42
	):
		self._num_threads = num_threads
		self._wikipedia = wikipedia
		self._echo = echo
		self._cache = cache
		self._create_cached_functions()
		self._pensieve = Pensieve()
		self._all_data = None

		self.pensieve.store(
			key='all_data', function=lambda :self.get_all(echo=echo),
			evaluate=False
		)
		self.pensieve['random_state'] = random_state
		self.pensieve['sample_size'] = sample_size
		self.pensieve['different_type_ratio'] = different_type_ratio
		self.pensieve.store(
			key='sample',
			function=lambda all_data, sample_size, different_type_ratio, random_state:
				self.get_entity_sample(
					size=sample_size, ratio=different_type_ratio, data=all_data,
					random_state=random_state, echo=echo
				),
			evaluate=False
		)




		def add_signatures(sample, echo):
			result = {}
			for key, data in sample.items():
				print(key)
				new_data = data.copy()
				urls = list(new_data['url'])
				progress_bar = ProgressBar(total=len(urls) + 1, echo=echo)
				signatures = self.processor(
					delayed(self.get_page_signature)(url)
					for url in iterate(
						iterable=urls, progress_bar=progress_bar, text=f'collecting {key} signatures'
					)
				)
				progress_bar.show(amount=len(urls) + 1, text='signatures_collected')
				new_data['signature'] = signatures

				result[key] = new_data
			return result
		self.pensieve.store(
			key='signatures', function=lambda sample: add_signatures(sample=sample, echo=echo),
			evaluate=False
		)

	@property
	def processor(self):
		return Parallel(n_jobs=self._num_threads, backend='threading', require='sharedmem')

	@property
	def pensieve(self):
		"""
		:rtype: Pensieve
		"""
		return self._pensieve

	_STATE_ATTRIBUTES_ = ['_wikipedia', '_echo', '_cache']

	def __getstate__(self):
		return {key: getattr(self, key) for key in self._STATE_ATTRIBUTES_}

	def __setstate__(self, state):
		for key, value in state.items():
			setattr(self, key, value)
		self._create_cached_functions()

	def __hashkey__(self):
		return self.__class__.__name__, self._wikipedia, self._cache

	def _get_page_signature(self, url):
		if url.startswith('https://en.wikipedia.org/wiki/') and \
				'#' not in url and 'index.php?' not in url and '/wiki/file:' not in url.lower():
			try:
				signature = PageSignature(wikipedia=self._wikipedia, url=url)
				return signature.signature
			except Exception as e:
				return {'error': str(e)}
		else:
			return {'error': 'bad_url'}

	@property
	def cache(self):
		"""
		:rtype: Cache
		"""
		return self._cache

	def _create_cached_functions(self):
		if self.cache:
			self.get_data = self.cache.make_cached(
				function=self._get_data, id='WikipediaEntities.get_data',
				sub_directory='entities_data', exclude_kwargs=['echo']
			)
			self.get_page_signature = self.cache.make_cached(
				function=self._get_page_signature, id='WikipediaEntities.get_page_signature',
				sub_directory='entities_signature',
				condition_function=lambda result: 'error' in result and len(result) < 2
			)

		else:
			self.get_data = self._get_data
			self.get_page_signature = self._get_page_signature

	def _get_data(self, entity_type, echo=0):
		return get_data(entity_type=entity_type, wikipedia=self._wikipedia, echo=echo)

	@property
	def types(self):
		return list(KEYS)

	def keys(self):
		return self.types

	def __getitem__(self, item):
		return self.get_data(entity_type=item, echo=0)

	def get_all(self, echo=1):
		"""
		:type echo: bool or int or ProgressBar
		:rtype: pandas.DataFrame
		"""
		if self._all_data is None:
			echo=max(0, echo)
			result = []
			progress_bar = ProgressBar(total=len(self.types), echo=echo)
			progress = 0
			for entity_type in self.types:
				progress_bar.show(amount=progress, text=entity_type)
				data = self.get_data(entity_type=entity_type, echo=progress_bar-1)
				result.append(data)
				progress += 1
			progress_bar.show(amount=progress)
			self._all_data = concat(result).reset_index(drop=True)
		return self._all_data

	def get_entity_sample(self, size, ratio, data=None, echo=2, random_state=42):
		echo = max(0, echo)
		progress_bar = ProgressBar(total=None, echo=echo)

		if data is None:
			data = self.get_all(echo=progress_bar)

		data = data.sample(frac=1, random_state=random_state)
		counts = data['data_type'].value_counts().to_dict()
		other_size = round(size * ratio)

		dictionary = {}

		progress_bar.set_total(len(counts) * (len(counts) - 1))
		progress_amount = 0
		for main_data_type, count in counts.items():

			result = []
			this_data = data[data['data_type'] == main_data_type]
			if count > size:
				result.append(this_data.head(size))
			else:
				result.append(concat([this_data] * ceil(size / count)).head(size))

			for other_data_type, other_count in counts.items():
				if other_data_type != main_data_type:
					progress_bar.show(amount=progress_amount, text=f'{main_data_type}/{other_data_type}')
					progress_amount += 1
					other_data = data[data['data_type'] == other_data_type]
					if other_count > other_size:
						result.append(other_data.head(other_size))
					else:
						result.append(concat([other_data] * ceil(other_size / other_count)).head(other_size))

			dictionary[main_data_type] = concat(result)

		progress_bar.show(amount=progress_amount, text='sample complete!')

		return dictionary
