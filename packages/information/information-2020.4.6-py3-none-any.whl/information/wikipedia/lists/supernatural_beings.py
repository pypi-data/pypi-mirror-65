from ..WikipediaListGuide import WikipediaListGuide
from ..WikipediaLists import WikipediaLists
from chronometry.progress import ProgressBar


MYTH = 'mythological_figure'


def get_supernatural_beings(wikipedia=None, echo=0):
	echo = max(0, echo)
	progress_bar = ProgressBar(echo=echo, total=None)
	return WikipediaLists(
		echo=progress_bar,
		wikipedia_lists={
			'germanic_deities': WikipediaListGuide(
				list_type='list',
				wikipedia=wikipedia, echo=progress_bar - 1, data_type=MYTH,
				categories=[MYTH, 'deity', 'germanic', 'germanic_deity'],
				urls='https://en.wikipedia.org/wiki/List_of_Germanic_deities',
				columns={MYTH: ['name']}
			),
			'greek_mythological_figures': WikipediaListGuide(
				list_type='list',
				wikipedia=wikipedia, echo=progress_bar - 1, data_type=MYTH,
				categories=[MYTH, 'greek', 'greek_mythological_figure'],
				urls='https://en.wikipedia.org/wiki/List_of_Greek_mythological_figures'
			),
			'hindu_creatures': WikipediaListGuide(
				list_type='list',
				wikipedia=wikipedia, echo=progress_bar - 1, data_type=MYTH,
				categories=[MYTH, 'hindu', 'hindu_mythological_figure'],
				urls='https://en.wikipedia.org/wiki/List_of_legendary_creatures_in_Hindu_mythology'
			),
			'roman_deities': WikipediaListGuide(
				list_type='list',
				wikipedia=wikipedia, echo=progress_bar - 1, data_type=MYTH,
				categories=[MYTH, 'roman', 'roman_deity'],
				urls=['https://en.wikipedia.org/wiki/List_of_Roman_deities']
			),
			'legendary_creatures': WikipediaListGuide(
				list_type='list_of_lists',
				wikipedia=wikipedia, echo=progress_bar - 1, data_type=MYTH,
				categories=[MYTH, 'legendary_creature'],
				urls='https://en.wikipedia.org/wiki/Lists_of_legendary_creatures',
				representation='list'
			)
		}
	)
