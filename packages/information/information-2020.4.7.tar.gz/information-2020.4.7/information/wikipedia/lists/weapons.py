from ..WikipediaListGuide import WikipediaListGuide
from ..WikipediaLists import WikipediaLists
from chronometry.progress import ProgressBar

WEAPON = 'weapon'


def get_weapons(wikipedia=None, echo=0):
	echo = max(0, echo)
	progress_bar = ProgressBar(echo=echo, total=None)
	return WikipediaLists(
		echo=progress_bar,
		wikipedia_lists={
			'weapons': WikipediaListGuide(
				list_type='list_of_lists',
				wikipedia=wikipedia, echo=progress_bar - 1, data_type=WEAPON, categories=[WEAPON],
				urls=[
					'https://en.wikipedia.org/wiki/Lists_of_weapons',
					'https://en.wikipedia.org/wiki/List_of_World_War_II_weapons',
					'https://en.wikipedia.org/wiki/Lists_of_rockets',
					'https://en.wikipedia.org/wiki/Lists_of_swords',
					'https://en.wikipedia.org/wiki/Draft:List_of_service_rifles',
					'https://en.wikipedia.org/wiki/List_of_assault_rifles',
					'https://en.wikipedia.org/wiki/List_of_aircraft_carriers_of_the_United_States_Navy',
					'https://en.wikipedia.org/wiki/List_of_active_United_States_military_aircraft',
					'https://en.wikipedia.org/wiki/List_of_submarines_of_the_United_States_Navy',
					'https://en.wikipedia.org/wiki/List_of_active_Indian_military_aircraft',
					'https://en.wikipedia.org/wiki/Lists_of_armoured_fighting_vehicles'
				],
				exclude_urls=[
					'https://en.wikipedia.org/wiki/List_of_firearms',
					'https://en.wikipedia.org/wiki/List_of_National_Treasures_of_Japan_(crafts:_swords)',
					'https://en.wikipedia.org/wiki/List_of_fictional_swords',
					'https://en.wikipedia.org/wiki/Classification_of_swords'
				],
				columns={WEAPON: ['model', 'name', 'type', 'name_designation', 'firearm', 'aircraft']}
			),
			'tanks': WikipediaListGuide(
				list_type='list',
				wikipedia=wikipedia, echo=progress_bar - 1, data_type=WEAPON, categories=[WEAPON],
				urls=[
					'https://en.wikipedia.org/wiki/List_of_main_battle_tanks_by_generation',
					'https://en.wikipedia.org/wiki/List_of_tanks_of_the_Soviet_Union',
					'https://en.wikipedia.org/wiki/List_of_tanks_of_the_United_Kingdom',
					'https://en.wikipedia.org/wiki/List_of_main_battle_tanks_by_country'
				],
				columns={WEAPON: ['model', 'name', 'type', 'name_designation', 'firearm', 'aircraft']}
			)
		}
	)
