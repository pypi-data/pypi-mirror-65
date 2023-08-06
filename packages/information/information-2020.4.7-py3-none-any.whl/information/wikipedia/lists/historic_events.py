from ..WikipediaListGuide import WikipediaListGuide
from ..WikipediaLists import WikipediaLists
from chronometry.progress import ProgressBar


HISTORIC_EVENT = 'historic_event'

def get_historic_events(wikipedia=None, echo=0):
	echo = max(0, echo)
	progress_bar = ProgressBar(echo=echo, total=None)

	battles_and_disasters = {
		'by_period': WikipediaListGuide(
			list_type='list', data_type=HISTORIC_EVENT, echo=progress_bar - 1,
			wikipedia=wikipedia, categories=[HISTORIC_EVENT, 'battle'],
			representation=None,
			columns={HISTORIC_EVENT: ['name', 'battle']},
			urls=[
				'https://en.wikipedia.org/wiki/List_of_battles_before_301',
				'https://en.wikipedia.org/wiki/List_of_battles_301–1300',
				'https://en.wikipedia.org/wiki/List_of_battles_1301%E2%80%931600',
				'https://en.wikipedia.org/wiki/List_of_battles_1601%E2%80%931800',
				'https://en.wikipedia.org/wiki/List_of_battles_1801%E2%80%931900',
				'https://en.wikipedia.org/wiki/List_of_battles_1901%E2%80%932000',
				'https://en.wikipedia.org/wiki/List_of_battles_since_2001',


			]
		),
		'american_revolutionary_war': WikipediaListGuide(
			list_type='list', data_type=HISTORIC_EVENT, echo=progress_bar - 1,
			wikipedia=wikipedia, categories=[HISTORIC_EVENT, 'battle', 'american_revolution'],
			representation='table',
			columns={HISTORIC_EVENT: ['name', 'battle']},
			urls=[
				'https://en.wikipedia.org/wiki/List_of_American_Revolutionary_War_battles'
			]
		),
		'american_civil_war_battles': WikipediaListGuide(
			list_type='list', data_type=HISTORIC_EVENT, echo=progress_bar - 1,
			wikipedia=wikipedia, categories=[HISTORIC_EVENT, 'battle', 'american_civil_war'],
			representation='table',
			columns={HISTORIC_EVENT: ['name', 'battle']},
			urls=[
				'https://en.wikipedia.org/wiki/List_of_American_Civil_War_battles'
			]
		),
		'napoleonic_battles': WikipediaListGuide(
			list_type='list', data_type=HISTORIC_EVENT, echo=progress_bar - 1,
			wikipedia=wikipedia, categories=[HISTORIC_EVENT, 'battle', 'napoleonic_war'],
			representation='list',
			urls=[
				'https://en.wikipedia.org/wiki/List_of_Napoleonic_battles'
			]
		),
		'world_war_1': WikipediaListGuide(
			list_type='list', data_type=HISTORIC_EVENT, echo=progress_bar - 1,
			wikipedia=wikipedia, categories=[HISTORIC_EVENT, 'battle', 'world_war_1'],
			representation='list',
			urls=[
				'https://en.wikipedia.org/wiki/List_of_military_engagements_of_World_War_I'
			]
		),
		'world_war_2': WikipediaListGuide(
			list_type='list', data_type=HISTORIC_EVENT, echo=progress_bar - 1,
			wikipedia=wikipedia, categories=[HISTORIC_EVENT, 'battle', 'world_war_2'],
			representation='list',
			urls=[
				'https://en.wikipedia.org/wiki/List_of_military_engagements_of_World_War_II'
			]
		),
		'battles_by_casualties': WikipediaListGuide(
			list_type='list', data_type=HISTORIC_EVENT, echo=progress_bar - 1,
			wikipedia=wikipedia, categories=[HISTORIC_EVENT, 'battle'],
			representation='table',
			columns={HISTORIC_EVENT: ['battle', 'operation']},
			urls=[
				'https://en.wikipedia.org/wiki/List_of_battles_by_casualties'
			]
		),
		'sieges_by_casualties': WikipediaListGuide(
			list_type='list', data_type=HISTORIC_EVENT, echo=progress_bar - 1,
			wikipedia=wikipedia, categories=[HISTORIC_EVENT, 'siege', 'battle'],
			representation='table',
			columns={HISTORIC_EVENT: ['siege']},
			urls=[
				'https://en.wikipedia.org/wiki/List_of_battles_by_casualties'
			]
		),
		'wars_by_casualties': WikipediaListGuide(
			list_type='list', data_type=HISTORIC_EVENT, echo=progress_bar - 1,
			wikipedia=wikipedia, categories=[HISTORIC_EVENT, 'war'],
			representation='table',
			columns={HISTORIC_EVENT: ['conflict', 'name_of_conflict']},
			urls=[
				'https://en.wikipedia.org/wiki/List_of_battles_by_casualties',
				'https://en.wikipedia.org/wiki/List_of_wars:_2003%E2%80%93present'
			]
		),
		'disasters': WikipediaListGuide(
			list_type='list', data_type=HISTORIC_EVENT, echo=progress_bar - 1,
			wikipedia=wikipedia, categories=[HISTORIC_EVENT, 'disaster'],
			representation='table',
			columns={HISTORIC_EVENT: ['event']},
			urls=[
				'https://en.wikipedia.org/wiki/List_of_wars_and_anthropogenic_disasters_by_death_toll'
			]
		),
		'disasters_2': WikipediaListGuide(
			list_type='list_of_lists', data_type=HISTORIC_EVENT, echo=progress_bar - 1,
			wikipedia=wikipedia, categories=[HISTORIC_EVENT, 'disaster'],
			representation=None,
			columns={HISTORIC_EVENT: ['event']},
			urls=[
				'https://en.wikipedia.org/wiki/Lists_of_disasters'
			],
			sections=['Natural disasters'],
			exclude_list_pages=[
				'https://en.wikipedia.org/wiki/List_of_accidents_and_incidents_involving_commercial_aircraft',
				'https://en.wikipedia.org/wiki/List_of_accidents_and_incidents_involving_military_aircraft',
				'https://en.wikipedia.org/wiki/List_of_airship_accidents',

			]
		),
		'massacres': WikipediaListGuide(
			list_type='list', data_type=HISTORIC_EVENT, echo=progress_bar - 1,
			wikipedia=wikipedia, categories=[HISTORIC_EVENT, 'massacre'],
			representation='table',
			columns={HISTORIC_EVENT: ['name']},
			urls=[
				'https://en.wikipedia.org/wiki/List_of_events_named_massacres',
				'https://en.wikipedia.org/wiki/List_of_massacres_in_the_United_States'
			]
		),
		'genocides': WikipediaListGuide(
			list_type='list', data_type=HISTORIC_EVENT, echo=progress_bar - 1,
			wikipedia=wikipedia, categories=[HISTORIC_EVENT, 'genocide'],
			representation='table',
			columns={HISTORIC_EVENT: ['event']},
			urls=[
				'https://en.wikipedia.org/wiki/List_of_genocides_by_death_toll'
			]
		),
		'earthquakes': WikipediaListGuide(
			list_type='list', data_type=HISTORIC_EVENT, echo=progress_bar - 1,
			wikipedia=wikipedia, categories=[HISTORIC_EVENT, 'natural_disaster', 'earthquake'],
			representation='table',
			columns={HISTORIC_EVENT: ['event']},
			urls=[
				'https://en.wikipedia.org/wiki/List_of_21st-century_earthquakes',
				'https://en.wikipedia.org/wiki/List_of_20th-century_earthquakes'
			]
		),
		'natural_disasters': WikipediaListGuide(
			list_type='list', data_type=HISTORIC_EVENT, echo=progress_bar - 1,
			wikipedia=wikipedia, categories=[HISTORIC_EVENT, 'disaster', 'natural_disaster'],
			representation='table',
			columns={HISTORIC_EVENT: ['event']},
			urls=[
				'https://en.wikipedia.org/wiki/List_of_natural_disasters_by_death_toll'
			]
		),
		'terrorist_attacks': WikipediaListGuide(
			list_type='list', data_type=HISTORIC_EVENT, echo=progress_bar - 1,
			wikipedia=wikipedia, categories=[HISTORIC_EVENT, 'disaster', 'terrorist_attack'],
			representation='table',
			columns={HISTORIC_EVENT: ['name']},
			urls=[
				'https://en.wikipedia.org/wiki/List_of_battles_and_other_violent_events_by_death_toll'
			],
			sections=['Terrorist attacks']
		),
		'riots': WikipediaListGuide(
			list_type='list', data_type=HISTORIC_EVENT, echo=progress_bar - 1,
			wikipedia=wikipedia, categories=[HISTORIC_EVENT, 'disaster', 'riot'],
			representation='table',
			columns={HISTORIC_EVENT: ['name']},
			urls=[
				'https://en.wikipedia.org/wiki/List_of_battles_and_other_violent_events_by_death_toll'
			],
			sections=['Mass unrest, riots and pogroms']
		),
		'rail_accidents': WikipediaListGuide(
			list_type='list', data_type=HISTORIC_EVENT, echo=progress_bar - 1,
			wikipedia=wikipedia, categories=[HISTORIC_EVENT, 'disaster', 'rail_accident'],
			representation='table',
			columns={HISTORIC_EVENT: ['name']},
			urls=[
				'https://en.wikipedia.org/wiki/List_of_battles_and_other_violent_events_by_death_toll'
			],
			sections=['Mass unrest, riots and pogroms']
		),
	}

	by_country_dictionary = {
		'swedish_battle': 'https://en.wikipedia.org/wiki/List_of_Swedish_battles',
		'american_battle': 'https://en.wikipedia.org/wiki/List_of_battles_with_most_United_States_military_fatalities',
		'chinese_battle': 'https://en.wikipedia.org/wiki/List_of_Chinese_wars_and_battles',
		'french_battle': [
			'https://en.wikipedia.org/wiki/List_of_battles_involving_France_in_the_Middle_Ages',
			'https://en.wikipedia.org/wiki/List_of_battles_involving_France_in_the_Renaissance',
			'https://en.wikipedia.org/wiki/List_of_battles_involving_France_in_the_Ancien_R%C3%A9gime',
			'https://en.wikipedia.org/wiki/List_of_battles_involving_France_in_modern_history'
		],
		'indian_battle': 'https://en.wikipedia.org/wiki/List_of_Indian_battles',
		'japanese_battle': 'https://en.wikipedia.org/wiki/List_of_Japanese_battles',
		'korean_battle': 'https://en.wikipedia.org/wiki/List_of_Korean_battles',
		'prussian_battle': 'https://en.wikipedia.org/wiki/Wars_and_battles_involving_Prussia',
		'roman_war': 'https://en.wikipedia.org/wiki/List_of_Roman_wars_and_battles',
		'byzantine_battle': 'https://en.wikipedia.org/wiki/List_of_Byzantine_battles',
		'middle_east_conflict': 'https://en.wikipedia.org/wiki/List_of_modern_conflicts_in_the_Middle_East'
	}

	by_country = {
		country: WikipediaListGuide(
			list_type='list', data_type=HISTORIC_EVENT, echo=progress_bar - 1,
			wikipedia=wikipedia, categories=[HISTORIC_EVENT, 'battle', country],
			representation=None,
			columns={HISTORIC_EVENT: ['battle_or_siege', 'event', 'battle']},
			urls=url
		)
		for country, url in by_country_dictionary.items()
	}

	return WikipediaLists(
		echo=progress_bar,
		wikipedia_lists={**battles_and_disasters, **by_country}
	)

