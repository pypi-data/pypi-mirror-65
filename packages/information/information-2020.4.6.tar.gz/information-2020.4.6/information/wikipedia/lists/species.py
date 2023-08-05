from ..WikipediaListGuide import WikipediaListGuide
from .. WikipediaLists import WikipediaLists
from chronometry.progress import ProgressBar

SPECIES = 'species'


def get_domesticated_animals(wikipedia=None, echo=0):
	return {'domesticated_animals': WikipediaListGuide(
		list_type='list',
		wikipedia=wikipedia, echo=echo - 1, categories=[SPECIES, 'animal', 'domesticated'],
		data_type=SPECIES,
		urls='https://en.wikipedia.org/wiki/List_of_domesticated_animals',
		representation='table',
		columns={SPECIES: ['animal', 'animal_name', 'species_and_subspecies']}
	)}


def get_pests(wikipedia=None, echo=0):
	return {'common_household_pests': WikipediaListGuide(
		list_type='list',
		wikipedia=wikipedia, echo=echo - 1, categories=[SPECIES, 'animal', 'pest'],
		data_type=SPECIES,
		urls='https://en.wikipedia.org/wiki/List_of_common_household_pests',
		representation='table',
		columns={SPECIES: ['animal', 'animal_name', 'species_and_subspecies']}
	)}


def get_herbivores(wikipedia=None, echo=0):
	return {'herbivorous_animals': WikipediaListGuide(
		list_type='list',
		wikipedia=wikipedia, echo=echo - 1, categories=[SPECIES, 'animal', 'herbivore'],
		data_type=SPECIES,
		urls='https://en.wikipedia.org/wiki/List_of_herbivorous_animals',
		representation='table',
		columns={SPECIES: ['animal', 'animal_name', 'species_and_subspecies']}
	)}


def get_animals(wikipedia=None, echo=0):
	return {'animal_names': WikipediaListGuide(
		list_type='list',
		wikipedia=wikipedia, echo=echo - 1, categories=[SPECIES, 'animal'],
		data_type=SPECIES,
		urls=[
			'https://en.wikipedia.org/wiki/List_of_animal_names',
			'https://en.wikipedia.org/wiki/List_of_English_animal_nouns',

		],
		representation='table',
		columns={SPECIES: ['animal', 'animal_name', 'species_and_subspecies']}
	)}


def get_dinosaurs(wikipedia=None, echo=0):
	return {'dinosaur': WikipediaListGuide(
		list_type='list',
		wikipedia=wikipedia, echo=echo - 1, categories=[SPECIES, 'animal', 'dinosaur'],
		data_type=SPECIES,
		urls='https://en.wikipedia.org/wiki/List_of_dinosaur_genera',
		representation='list'
	)}


def get_extinct_mammals(wikipedia=None, echo=0):
	return {'extinct_mammals': WikipediaListGuide(
		list_type='list',
		wikipedia=wikipedia, echo=echo - 1, categories=[SPECIES, 'animal', 'mammal', 'extinct', 'extinct_mammal'],
		data_type=SPECIES,
		urls=[
			'https://en.wikipedia.org/wiki/List_of_recently_extinct_mammals',
			'https://en.wikipedia.org/wiki/List_of_extinct_cetaceans',
			'https://en.wikipedia.org/wiki/List_of_fossil_primates',
			'https://en.wikipedia.org/wiki/Category:Extinct_mammals'
		],
		columns={SPECIES: ['common_name']}
	)}


def get_extinct_birds(wikipedia=None, echo=0):
	return {'extinct_bird': WikipediaListGuide(
		list_type='list',
		wikipedia=wikipedia, echo=echo - 1, categories=[SPECIES, 'animal', 'bird', 'extinct', 'extinct_bird'],
		data_type=SPECIES,
		urls='https://en.wikipedia.org/wiki/List_of_recently_extinct_bird_species',
		representation='list'
	)}


def get_extinct_species(wikipedia=None, echo=0):
	return {'extinct_species': WikipediaListGuide(
		list_type='list_of_lists',
		wikipedia=wikipedia, echo=echo - 1, categories=[SPECIES, 'extinct'],
		data_type=SPECIES,
		urls=[
			'https://en.wikipedia.org/wiki/Lists_of_extinct_animals',
			'https://en.wikipedia.org/wiki/Lists_of_extinct_species'
		],
		columns={SPECIES: ['common_name', 'scientific_name', SPECIES]}
	)}


def get_mammals(wikipedia=None, echo=0):
	return {
		'mammals': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=echo - 1, categories=[SPECIES, 'animal', 'mammal'],
			data_type=SPECIES,
			urls=[
				'https://en.wikipedia.org/wiki/List_of_even-toed_ungulates_by_population',
				'https://en.wikipedia.org/wiki/List_of_carnivorans_by_population',
				'https://en.wikipedia.org/wiki/List_of_cetacean_species',
				'https://en.wikipedia.org/wiki/List_of_bats_by_population',
				'https://en.wikipedia.org/wiki/List_of_odd-toed_ungulates_by_population',
				'https://en.wikipedia.org/wiki/List_of_primates_by_population'
			],
			representation='table',
			columns={SPECIES: ['common_name']}
		),
		'primates': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=echo - 1, categories=[SPECIES, 'animal', 'mammal', 'primate'],
			data_type=SPECIES,
			urls=[
				'https://en.wikipedia.org/wiki/List_of_primates_by_population'
			],
			representation='table',
			columns={SPECIES: ['common_name']}
		)
	}


def get_plants(wikipedia=None, echo=0):
	return {'plants': WikipediaListGuide(
		list_type='list',
		wikipedia=wikipedia, echo=echo - 1, categories=[SPECIES, 'plant'],
		data_type=SPECIES,
		urls=[
			'https://en.wikipedia.org/wiki/Lists_of_cultivars'
		],
		columns={SPECIES: ['common_name']}
	)}


def get_species(wikipedia=None, echo=0):
	echo = max(0, echo)
	progress_bar = ProgressBar(echo=echo, total=None)
	return WikipediaLists(
		echo=progress_bar,
		wikipedia_lists={
			**get_animals(wikipedia=wikipedia, echo=progress_bar),
			**get_domesticated_animals(wikipedia=wikipedia, echo=progress_bar),
			**get_herbivores(wikipedia=wikipedia, echo=progress_bar),
			**get_pests(wikipedia=wikipedia, echo=progress_bar),
			**get_mammals(wikipedia=wikipedia, echo=progress_bar),
			**get_dinosaurs(wikipedia=wikipedia, echo=progress_bar),
			**get_extinct_mammals(wikipedia=wikipedia, echo=progress_bar),
			**get_extinct_species(wikipedia=wikipedia, echo=progress_bar),
			**get_plants(wikipedia=wikipedia, echo=progress_bar),
			**get_extinct_birds(wikipedia=wikipedia, echo=progress_bar)
		}
	)


def get_breeds(wikipedia=None, echo=0):
	echo = max(0, echo)
	progress_bar = ProgressBar(echo=echo, total=None)
	return WikipediaLists(
		echo=progress_bar,
		wikipedia_lists={
			'cat_breeds': WikipediaListGuide(
				list_type='list',
				wikipedia=wikipedia, echo=echo - 1, categories=['breed', 'cat', 'cat_breed', 'animal', 'mammal'],
				data_type='breed',
				urls='https://en.wikipedia.org/wiki/List_of_cat_breeds',
				columns={'breed': ['breed']}
			),
			'dog_breeds': WikipediaListGuide(
				list_type='list',
				wikipedia=wikipedia, echo=echo - 1, categories=['breed', 'dog', 'dog_breed', SPECIES, 'animal', 'mammal'],
				data_type='breed',
				urls='https://en.wikipedia.org/wiki/List_of_dog_breeds',
				columns={'breed': ['breed']}
			),
			'akc_breeds': WikipediaListGuide(
				list_type='list',
				wikipedia=wikipedia, echo=echo - 1, categories=['breed', 'dog', 'dog_breed', SPECIES, 'animal', 'mammal'],
				data_type='breed',
				urls='https://en.wikipedia.org/wiki/American_Kennel_Club',
				representation='list',
				sections=['Recognized breeds']
			),
			'ckc_breeds': WikipediaListGuide(
				list_type='list',
				wikipedia=wikipedia, echo=echo - 1, categories=['breed', 'dog', 'dog_breed', SPECIES, 'animal', 'mammal'],
				data_type='breed',
				urls='https://en.wikipedia.org/wiki/Canadian_Kennel_Club',
				representation='list'
			),
			'horse_breeds': WikipediaListGuide(
				list_type='list',
				wikipedia=wikipedia, echo=echo - 1, categories=['breed', 'horse', 'horse_breed', SPECIES, 'animal', 'mammal'],
				data_type='breed',
				urls=[
					'https://en.wikipedia.org/wiki/List_of_horse_breeds',
					'https://en.wikipedia.org/wiki/List_of_gaited_horse_breeds',
					'https://en.wikipedia.org/wiki/List_of_Brazilian_horse_breeds',
					'https://en.wikipedia.org/wiki/List_of_French_horse_breeds',
					'https://en.wikipedia.org/wiki/List_of_Italian_horse_breeds'
				],
				representation='list'
			)
		}
	)
