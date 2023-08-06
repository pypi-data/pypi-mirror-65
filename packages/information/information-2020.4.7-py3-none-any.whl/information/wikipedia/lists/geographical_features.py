from ..WikipediaListGuide import WikipediaListGuide
from ..WikipediaLists import WikipediaLists
from chronometry.progress import ProgressBar

GEOGRAPHICAL_FEATURE = 'geographical_feature'


def get_geographical_feature_guides(wikipedia=None, echo=0):
	return {
		'oceans': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=echo - 1, categories=[GEOGRAPHICAL_FEATURE, 'body_of_water', 'ocean'],
			data_type=GEOGRAPHICAL_FEATURE,
			urls='https://en.wikipedia.org/wiki/Ocean',
			columns={GEOGRAPHICAL_FEATURE: ['ocean']},
			representation='table'
		),
		'seas': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=echo - 1, categories=[GEOGRAPHICAL_FEATURE, 'body_of_water', 'sea'],
			data_type=GEOGRAPHICAL_FEATURE,
			urls='https://en.wikipedia.org/wiki/List_of_seas',
			representation='list'
		),
		'lakes': WikipediaListGuide(
			list_type='list_of_lists',
			wikipedia=wikipedia, echo=echo - 1, categories=[GEOGRAPHICAL_FEATURE, 'body_of_water', 'lake'],
			data_type=GEOGRAPHICAL_FEATURE,
			urls=[
				'https://en.wikipedia.org/wiki/Lists_of_lakes',
				'https://en.wikipedia.org/wiki/Lists_of_lakes_of_Western_Australia'
			],
			columns={GEOGRAPHICAL_FEATURE: ['name', 'lake', 'lake_name', 'lake_or_reservoir']}
		),
		'rivers': WikipediaListGuide(
			list_type='list_of_lists',
			wikipedia=wikipedia, echo=echo - 1, categories=[GEOGRAPHICAL_FEATURE, 'body_of_water', 'river'],
			data_type=GEOGRAPHICAL_FEATURE,
			urls=[
				'https://en.wikipedia.org/wiki/Lists_of_rivers',
				'https://en.wikipedia.org/wiki/Lists_of_rivers_of_U.S._insular_areas',
				'https://en.wikipedia.org/wiki/List_of_peaks_by_prominence',
				'https://en.wikipedia.org/wiki/Seven_Summits',

			],
			columns={GEOGRAPHICAL_FEATURE: ['river', 'name', 'name_of_river', 'modern_name', 'peak']}
		),
		'mountain_ranges': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=echo - 1, categories=[GEOGRAPHICAL_FEATURE, 'mountain_range'],
			data_type=GEOGRAPHICAL_FEATURE,
			urls='https://en.wikipedia.org/wiki/List_of_mountain_ranges',
			representation='list'
		),
		'mountains': WikipediaListGuide(
			list_type='list_of_lists',
			wikipedia=wikipedia, echo=echo - 1, categories=[GEOGRAPHICAL_FEATURE, 'mountain'],
			data_type=GEOGRAPHICAL_FEATURE,
			urls=['https://en.wikipedia.org/wiki/Lists_of_mountains_by_region'],
			columns={GEOGRAPHICAL_FEATURE: ['mountain', 'peak', 'name', 'mountain_peak']}
		),
		'volcanos': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=echo - 1, categories=[GEOGRAPHICAL_FEATURE, 'mountain', 'volcano'],
			data_type=GEOGRAPHICAL_FEATURE,
			urls=[
				'https://en.wikipedia.org/wiki/List_of_large_volcanic_eruptions_of_the_19th_century',
				'https://en.wikipedia.org/wiki/List_of_large_volcanic_eruptions_of_the_20th_century',
				'https://en.wikipedia.org/wiki/List_of_large_volcanic_eruptions_in_the_21st_century',
				'https://en.wikipedia.org/wiki/List_of_volcanic_eruptions_by_death_toll'
			],
			columns={GEOGRAPHICAL_FEATURE: ['volcano', 'volcano_eruption']}
		)
	}

def get_geographical_features(wikipedia=None, echo=0):
	echo = max(0, echo)
	progress_bar = ProgressBar(echo=echo, total=None)
	return WikipediaLists(
		wikipedia_lists=get_geographical_feature_guides(wikipedia=wikipedia, echo=progress_bar),
		echo=progress_bar
	)