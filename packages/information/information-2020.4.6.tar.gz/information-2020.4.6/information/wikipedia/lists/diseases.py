from ..WikipediaListGuide import WikipediaListGuide
from ..WikipediaLists import WikipediaLists
from chronometry.progress import ProgressBar


def get_diseases(wikipedia=None, echo=0):
	echo = max(0, echo)
	progress_bar = ProgressBar(echo=echo, total=None)

	return WikipediaLists(
		echo=progress_bar,
		wikipedia_lists={
			'diseases': WikipediaListGuide(
				list_type='list_of_lists',
				wikipedia=wikipedia, echo=progress_bar - 1, categories='disease',
				data_type='disease',
				urls='https://en.wikipedia.org/wiki/Lists_of_diseases',
				columns={'disease': ['common_name', 'disease', 'disorder']}
			)
		}
	)
