from ..WikipediaListGuide import WikipediaListGuide
from ..WikipediaLists import WikipediaLists
from chronometry.progress import ProgressBar

LANDMARK = 'landmark'


def get_landmarks(wikipedia=None, echo=0):
	urls_and_categories = [
		('https://en.wikipedia.org/wiki/List_of_tallest_buildings', ['building', 'tall_building']),
		('https://en.wikipedia.org/wiki/List_of_national_parks_of_the_United_States', ['park', 'national_park', 'united_states']),
		(
			[
				'https://en.wikipedia.org/wiki/List_of_eponyms_of_airports'
				'https://en.wikipedia.org/wiki/List_of_busiest_airports_by_passenger_traffic'
			],
			['airport']
		),
		('https://en.wikipedia.org/wiki/List_of_airports_in_China', ['airport', 'china']),
		('https://en.wikipedia.org/wiki/List_of_ports_in_the_United_States', ['port', 'united_states']),
		('https://en.wikipedia.org/wiki/List_of_ports_in_Ukraine', ['port', 'ukraine', 'europe']),
		('https://en.wikipedia.org/wiki/List_of_ports_in_Sri_Lanka', ['port', 'sri_lanka']),
		('https://en.wikipedia.org/wiki/List_of_ports_in_Spain', ['port', 'spain', 'europe']),
		('https://en.wikipedia.org/wiki/Ports_and_harbours_in_South_Africa', ['port', 'south_africa']),
		('https://en.wikipedia.org/wiki/List_of_ports_and_harbours_in_Scotland', ['port', 'scotland', 'europe']),
		('https://en.wikipedia.org/wiki/List_of_ports_in_Romania', ['port', 'romania', 'europe']),
		('https://en.wikipedia.org/wiki/Ports_in_India', ['port', 'india']),
		('https://en.wikipedia.org/wiki/List_of_Liverpool_Docks', ['dock', 'liverpool', 'united_kingdom', 'europe']),
		('https://en.wikipedia.org/wiki/List_of_ports_in_China', ['port', 'china']),
		('https://en.wikipedia.org/wiki/List_of_ports_in_Belgium', ['port', 'belgium', 'europe']),
		('https://en.wikipedia.org/wiki/List_of_ports_in_Australia', ['port', 'australia']),
		('https://en.wikipedia.org/wiki/List_of_ports_in_Argentina', ['port', 'argentina']),
		('https://en.wikipedia.org/wiki/List_of_ports_in_Albania', ['port', 'albania', 'europe']),
		('https://en.wikipedia.org/wiki/Iceport', ['port', 'iceport']),
		('https://en.wikipedia.org/wiki/List_of_busiest_ports_in_Europe', ['port', 'busy_port', 'europe']),
		('https://en.wikipedia.org/wiki/List_of_busiest_transshipment_ports', ['port', 'busy_port', 'transshipment_port']),
		('https://en.wikipedia.org/wiki/List_of_busiest_container_ports', ['port', 'busy_port', 'container_port'])
	]

	echo = max(0, echo)
	progress_bar = ProgressBar(echo=echo, total=None)

	return WikipediaLists(
		wikipedia_lists={
			(urls[0] if isinstance(urls, list) else urls): WikipediaListGuide(
				list_type='list',
				wikipedia=wikipedia, echo=progress_bar - 1, data_type=LANDMARK, categories=[LANDMARK] + categories,
				urls=urls,
				columns={LANDMARK: ['port_name', 'name', 'main_ports', 'tourism_ports']}
			)
			for urls, categories in urls_and_categories
		},
		echo=progress_bar
	)
