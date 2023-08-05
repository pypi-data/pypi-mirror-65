from ..WikipediaListGuide import WikipediaListGuide
from ..WikipediaLists import WikipediaLists
from chronometry.progress import ProgressBar

CHARACTER = 'fictional_character'


def get_fictional_characters(wikipedia=None, echo=0):
	echo = max(0, echo)
	progress_bar = ProgressBar(echo=echo, total=None)
	return WikipediaLists(
		echo=progress_bar,
		wikipedia_lists={
			'starwars_characters': WikipediaListGuide(
				list_type='list',
				wikipedia=wikipedia, echo=progress_bar - 1, data_type=CHARACTER,
				categories=[CHARACTER, 'starwars_character'],
				urls='https://en.wikipedia.org/wiki/List_of_Star_Wars_characters',
				columns={CHARACTER: 'name'}
			),
			'pokemon_characters': WikipediaListGuide(
				list_type='list',
				wikipedia=wikipedia, echo=progress_bar - 1, data_type=CHARACTER,
				categories=[CHARACTER, 'pokemon_character'],
				urls='https://en.wikipedia.org/wiki/List_of_generation_I_Pok%C3%A9mon',
				columns={CHARACTER: 'english_name'}
			),
			'coronation_street_characters': WikipediaListGuide(
				list_type='list',
				wikipedia=wikipedia, echo=progress_bar - 1, data_type=CHARACTER,
				categories=[CHARACTER, 'coronation_street_character'],
				urls='https://en.wikipedia.org/wiki/List_of_Coronation_Street_characters',
				columns={CHARACTER: 'character'}
			),
			'emmerdale_characters': WikipediaListGuide(
				list_type='list',
				wikipedia=wikipedia, echo=progress_bar - 1, data_type=CHARACTER,
				categories=[CHARACTER, 'emmerdale_character'],
				urls='https://en.wikipedia.org/wiki/List_of_Emmerdale_characters',
				columns={CHARACTER: 'character'}
			),
			'neighbours_characters': WikipediaListGuide(
				list_type='list',
				wikipedia=wikipedia, echo=progress_bar - 1, data_type=CHARACTER,
				categories=[CHARACTER, 'neighbours_character'],
				urls='https://en.wikipedia.org/wiki/List_of_Neighbours_characters',
				columns={CHARACTER: 'character'}
			),
			'the_simpsons_characters': WikipediaListGuide(
				list_type='list',
				wikipedia=wikipedia, echo=progress_bar - 1, data_type=CHARACTER,
				categories=[CHARACTER, 'the_simpsons_character'],
				urls='https://en.wikipedia.org/wiki/List_of_The_Simpsons_characters',
				columns={CHARACTER: 'character'}
			),
			'hollyoaks_characters': WikipediaListGuide(
				list_type='list',
				wikipedia=wikipedia, echo=progress_bar - 1, data_type=CHARACTER,
				categories=[CHARACTER, 'hollyoaks_character'],
				urls='https://en.wikipedia.org/wiki/List_of_Hollyoaks_characters',
				columns={CHARACTER: 'character'}
			),
			'x_men_characters': WikipediaListGuide(
				list_type='list',
				wikipedia=wikipedia, echo=progress_bar - 1, data_type=CHARACTER,
				categories=[CHARACTER, 'x_men_character'],
				urls='https://en.wikipedia.org/wiki/List_of_X-Men_members',
				columns={CHARACTER: 'character'}
			)
		}
	)
