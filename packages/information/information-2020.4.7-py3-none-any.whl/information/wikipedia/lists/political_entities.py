from ..WikipediaListGuide import WikipediaListGuide
from ..WikipediaLists import WikipediaLists
from chronometry.progress import ProgressBar


POLITICAL_ENTITY = 'political_entity'
COUNTRY = 'country'
STATE = 'state'

def get_political_entity_guides(wikipedia=None, echo=0):
	return {
		'countries_and_dependencies_by_population': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=echo - 1, categories=[POLITICAL_ENTITY, COUNTRY],
			data_type=POLITICAL_ENTITY,
			urls=[
				'https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population',
				'https://en.wikipedia.org/wiki/List_of_national_capitals'

			],
			columns={POLITICAL_ENTITY: ['country_or_dependent_territory', 'country_dependent_territory', 'country']}
		),
		'commonwealth_of_nations': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=echo - 1, categories=[POLITICAL_ENTITY, COUNTRY, 'commonwealth'],
			data_type=POLITICAL_ENTITY,
			urls='https://en.wikipedia.org/wiki/Member_states_of_the_Commonwealth_of_Nations',
			columns={POLITICAL_ENTITY: ['country']}
		),
		'national_capitals': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=echo - 1, categories=[POLITICAL_ENTITY, 'city', 'capital'],
			data_type=POLITICAL_ENTITY,
			urls='https://en.wikipedia.org/wiki/List_of_national_capitals',
			columns={POLITICAL_ENTITY: 'city'}
		),
		'states_and_territories_of_the_united_states': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=echo - 1, categories=[POLITICAL_ENTITY, STATE, 'united_states'],
			data_type=POLITICAL_ENTITY,
			urls='https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States_by_population',
			columns={POLITICAL_ENTITY: 'name'}
		),
		'states_of_mexico': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=echo - 1, categories=[POLITICAL_ENTITY, STATE, 'mexico'],
			data_type=POLITICAL_ENTITY,
			urls='https://en.wikipedia.org/wiki/List_of_states_of_Mexico',
			columns={POLITICAL_ENTITY: 'state'}
		),
		'cities_by_country': WikipediaListGuide(
			list_type='list_of_lists',
			wikipedia=wikipedia, echo=echo - 1, categories=[POLITICAL_ENTITY, 'city'],
			data_type=POLITICAL_ENTITY,
			urls=[
				'https://en.wikipedia.org/wiki/Lists_of_cities_by_country',
			],
			columns={POLITICAL_ENTITY: [
				'name', 'city_town', 'city', 'cities_towns', 'name_of_town_or_city', 'city_localidad', 'city_or_town',
				'cities', 'common_name', 'municipality', 'gccsa_sua', 'urban_area', 'municipio',
				'belarusian_bgn_pcgn', 'capital', 'english', 'settlement',
				'local_council'
			]}
		),
		'united_states_cities': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=echo - 1, categories=[POLITICAL_ENTITY, 'city', 'united_states'],
			data_type=POLITICAL_ENTITY,
			urls=[
				'https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population',
				'https://en.wikipedia.org/wiki/List_of_cities_and_towns_in_California',
				'https://en.wikipedia.org/wiki/List_of_cities_and_towns_in_Washington',
				'https://en.wikipedia.org/wiki/List_of_cities_and_towns_in_Arizona',
				'https://en.wikipedia.org/wiki/List_of_cities_in_West_Virginia',
				'https://en.wikipedia.org/wiki/List_of_cities_in_New_York_(state)'
			],
			columns={POLITICAL_ENTITY: [
				'name', 'city_town', 'city', 'cities_towns', 'name_of_town_or_city', 'city_localidad', 'city_or_town',
				'cities', 'common_name', 'municipality', 'gccsa_sua', 'urban_area', 'municipio',
				'belarusian_bgn_pcgn', 'capital', 'english', 'settlement',
				'local_council'
			]}
		),
		'municipalities_of_brazil': WikipediaListGuide(
			list_type='list_of_lists',
			wikipedia=wikipedia, echo=echo - 1, categories=[POLITICAL_ENTITY, 'city', 'municipality', 'brazil'],
			data_type=POLITICAL_ENTITY,
			urls='https://en.wikipedia.org/wiki/Municipalities_of_Brazil',
			columns={POLITICAL_ENTITY: ['municipality']}
		),
		'towns_in_india': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=echo - 1, categories=[POLITICAL_ENTITY, 'city', 'indian_town', 'india'],
			data_type=POLITICAL_ENTITY,
			urls='https://en.wikipedia.org/wiki/List_of_towns_in_India_by_population',
			columns={POLITICAL_ENTITY: 'name_of_town'}
		),
		'united_kingdom_locations': WikipediaListGuide(
			list_type='list_of_lists',
			wikipedia=wikipedia, echo=echo - 1, categories=[POLITICAL_ENTITY, 'place', 'place_in_united_kingdom', 'united_kingdom'],
			data_type=POLITICAL_ENTITY,
			urls='https://en.wikipedia.org/wiki/List_of_United_Kingdom_locations',
			columns={POLITICAL_ENTITY: ['location']}
		),
		'cities_in_germany': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=echo - 1, categories=[POLITICAL_ENTITY, 'city', 'german_city', 'germany'],
			data_type=POLITICAL_ENTITY,
			urls='https://en.wikipedia.org/wiki/List_of_cities_in_Germany_by_population',
			columns={POLITICAL_ENTITY: 'city'}
		),
		'cities_in_italy': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=echo - 1, categories=[POLITICAL_ENTITY, 'city', 'italian_city', 'italy'],
			data_type=POLITICAL_ENTITY,
			urls='https://en.wikipedia.org/wiki/List_of_cities_in_Italy',
			columns={POLITICAL_ENTITY: 'city'}
		),
		'coastal_settlements_of_the_mediterranean_sea': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=echo - 1, categories=[POLITICAL_ENTITY, 'city'],
			data_type=POLITICAL_ENTITY,
			urls=[
				'https://en.wikipedia.org/wiki/List_of_coastal_settlements_of_the_Mediterranean_Sea',
				'https://en.wikipedia.org/wiki/List_of_North_Sea_ports',
				'https://en.wikipedia.org/wiki/List_of_cities_and_towns_in_Romania',
				'https://en.wikipedia.org/wiki/List_of_cities_in_Ukraine',
				'https://en.wikipedia.org/wiki/List_of_largest_cities_in_Brazil',
				'https://en.wikipedia.org/wiki/List_of_cities_in_Nepal'
			],
			columns={POLITICAL_ENTITY: [
				'name', 'city_town', 'city', 'cities_towns', 'name_of_town_or_city', 'city_localidad', 'city_or_town',
				'cities', 'common_name', 'municipality', 'gccsa_sua', 'urban_area', 'municipio',
				'belarusian_bgn_pcgn', 'capital', 'english', 'settlement',
				'local_council'
			]}
		),
		'counties_in_the_united_states': WikipediaListGuide(
			list_type='list_of_lists',
			wikipedia=wikipedia, echo=echo - 1, categories=[POLITICAL_ENTITY, 'county', 'united_states'],
			data_type=POLITICAL_ENTITY,
			urls='https://en.wikipedia.org/wiki/Lists_of_counties_in_the_United_States',
			columns={POLITICAL_ENTITY: ['county', 'county_or_equivalent']}
		)
	}


def get_political_entities(wikipedia=None, echo=0):
	echo = max(0, echo)
	progress_bar = ProgressBar(echo=echo, total=None)

	return WikipediaLists(
		wikipedia_lists=get_political_entity_guides(wikipedia=wikipedia, echo=progress_bar),
		echo=progress_bar
	)