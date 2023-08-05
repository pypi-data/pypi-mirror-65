import pycountry
import pandas as pd
import re

from chronometry.progress import ProgressBar
from ravenclaw.wrangling import join_wisely

from linguistics.similarity import get_similarity
from .Country import Country

def _get_word_set(x):
	"""
	:type x: str
	:rtype: set of str
	"""
	try:
		x = x.replace("'s", "")
		result = set(re.split(pattern='[^a-zA-Z]+', string=x.lower()))
	except:
		return set()

	for common_words in ['of', 'and']:
		try:
			result.remove(common_words)
		except:
			pass
	return result


# create a dataframe of countries
class Countries:
	_NAME_COLUMNS = ['common_name', 'name', 'official_name']
	def __init__(self):
		self._countries_df = pd.DataFrame(data=[self._country_to_dict(country) for country in pycountry.countries])
		records = self._countries_df.to_dict(orient='records')
		self._alpha2_dict = {record['alpha_2']:record for record in records}
		self._alpha3_dict = {record['alpha_3']:record for record in records}
		self._name_dict = {record['name']:record for record in records}
		# lower letters:
		"""
		for col in self._NAME_COLUMNS:
			self._countries_df[f'{col}_lower_split'] = self._countries_df[col].apply(_get_word_set)
		"""

	@staticmethod
	def _country_to_dict(country):
		"""
		:type country: pycountry.countries.data_class
		:rtype: dict
		"""
		return country.__dict__['_fields']

	@property
	def data(self):
		return self._countries_df.copy()

	def convert_code_to_dict(self, alpha2=None, alpha3=None):
		if alpha2 is not None:
			return self._alpha2_dict[alpha2.upper()]
		elif alpha3 is not None:
			return self._alpha3_dict[alpha3.upper()]
		else:
			raise ValueError(f'either alpha2 or alphe3 should be given')


	def find_country(self, name, echo=False, _country_data=None):

		df = self.data if _country_data is None else _country_data

		scores = pd.DataFrame()
		for col in df.columns:
			if name in list(df[col].values):
				# no need to score names and stuff, just find the country
				result = dict(df[df[col]==name].iloc[0,:])
				result['match_score'] = 1
				return Country(result)
			else:
				scores[col] = df[col].apply(lambda x:get_similarity(
					s1=x, s2=name, case_sensitivity=0.1, first_char_weight=1.0
				))
		max_scores = scores.max(axis=1)
		df['match_score'] = max_scores
		if echo: print(df.sort_values(by='match_score', ascending=False).head())
		result = dict(df.iloc[max_scores.idxmax()])
		return Country(dictionary=result)

	def find_countries(self, names, echo=False, echo_text=''):

		country_data = self.data
		result = list(ProgressBar.map(
			iterable=names,
			function=lambda x:self.find_country(name=x, echo=False, _country_data=country_data),
			echo=echo - 1, text=echo_text
		))
		return result

	def convert_to_alpha_2(self, data, country_col, echo=False, echo_text=''):
		"""
		converts a country column to alpha_2 codes
		:type data: pd.DataFrame
		:type country_col: str
		:rtype: pd.DataFrame
		"""
		country_data = self.data
		country_data['result'] = country_data['alpha_2'].values
		country_data.columns = [f'__{column}__' for column in country_data.columns]
		left = data.copy()
		left['__order__'] = range(left.shape[0])
		country_data.head()
		result_list = []
		for column in country_data.columns:
			if column not in ['__result__', '__order__']:
				joined_data = join_wisely(
					left=left, right=country_data[[column, '__result__']],
					left_on=country_col, right_on=column, remove_duplicates=False
				)
				if joined_data['both'].shape[0] > 0:
					# remove the column that was used for matching (like __alpha_3__) and put the rest in the result_list
					both = joined_data['both']
					left = joined_data['left_only']
					result_list.append(both.drop(axis=1, labels=column))
					if echo: print(f'joined:{both.shape[0]} using {column.strip("_")} and {left.shape[0]} remains ...')
					# keep anything that is left for future joins


		# put all the matched results into one dataset, matching score is 1
		most_of_the_result = pd.concat(result_list)
		most_of_the_result['alpha_2_match_score'] = 1

		# use find countries on the rest:
		countries_left = self.find_countries(names=list(left[country_col]), echo=echo - 1, echo_text=echo_text)
		left['__result__'] = [country['alpha_2'] for country in countries_left]
		left['alpha_2_match_score'] = [country['match_score'] for country in countries_left]

		result = pd.concat([most_of_the_result, left])
		"""
		:type result: pd.DataFrame
		"""
		result.sort_values(by='__order__', inplace=True)
		result[country_col] = result['__result__'].values
		# avoid duplicates
		result = result[~result['__order__'].duplicated()]
		result.drop(axis=1, labels=['__result__', '__order__'], inplace=True)
		result.index = data.index
		return result

