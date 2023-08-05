from ..WikipediaListGuide import WikipediaListGuide
from ..WikipediaLists import WikipediaLists
from chronometry.progress import ProgressBar

SPACE_OBJECT = 'space_object'


def get_space_object_guides(wikipedia=None, echo=0):
	return {
		'solar_system_objects': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, categories=[SPACE_OBJECT, 'solar_system_object'],
			data_type=SPACE_OBJECT, echo=echo,
			urls='https://en.wikipedia.org/wiki/List_of_Solar_System_objects',
			representation='list'
		),
		'exoplanets': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, categories=[SPACE_OBJECT, 'exoplanet'],
			data_type=SPACE_OBJECT, echo=echo,
			urls='https://en.wikipedia.org/wiki/List_of_exoplanets_(full)',
			representation='table',
			columns={SPACE_OBJECT: ['name']}
		),
		'stars_by_constellation': WikipediaListGuide(
			list_type='list_of_lists',
			wikipedia=wikipedia, categories=[SPACE_OBJECT, 'star'],
			data_type=SPACE_OBJECT, echo=echo,
			urls='https://en.wikipedia.org/wiki/Lists_of_stars_by_constellation',
			representation='table',
			columns={SPACE_OBJECT: ['name']}
		),
		'constellations': WikipediaListGuide(
			list_type='list', wikipedia=wikipedia, categories=[SPACE_OBJECT, 'constellation'],
			data_type=SPACE_OBJECT, echo=echo,
			urls='https://en.wikipedia.org/wiki/IAU_designated_constellations',
			representation='table',
			columns={SPACE_OBJECT: ['constellation']}
		),
		'galaxies': WikipediaListGuide(
			list_type='list', wikipedia=wikipedia, categories=[SPACE_OBJECT, 'galaxy'],
			data_type=SPACE_OBJECT, echo=echo,
			urls='https://en.wikipedia.org/wiki/List_of_galaxies',
			representation='table',
			columns={SPACE_OBJECT: ['galaxy']}
		)
	}


def get_space_objects(wikipedia=None, echo=0):
	echo = max(0, echo)
	progress_bar = ProgressBar(echo=echo, total=None)
	list_guides = get_space_object_guides(wikipedia=wikipedia, echo=progress_bar - 1)
	return WikipediaLists(wikipedia_lists=list_guides, categories=[SPACE_OBJECT], echo=progress_bar - 1)
