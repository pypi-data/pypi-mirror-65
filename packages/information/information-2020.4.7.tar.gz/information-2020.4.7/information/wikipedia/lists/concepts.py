from ..WikipediaListGuide import WikipediaListGuide
from ..WikipediaLists import WikipediaLists
from chronometry.progress import ProgressBar

CONCEPT = 'concept'
LANGUAGE = 'language'


def get_concepts(wikipedia=None, echo=0):
	echo = max(0, echo)
	progress_bar = ProgressBar(echo=echo, total=None)
	
	return WikipediaLists(
		echo=progress_bar,
		wikipedia_lists={
			'warfare': WikipediaListGuide(
				list_type='list',
				wikipedia=wikipedia, echo=progress_bar - 1, data_type=CONCEPT,
				categories=[CONCEPT, 'warfare'],
				urls=['https://en.wikipedia.org/wiki/Outline_of_war'],
				representation='list',
				sections=['Types of war']
			),
			'languages': WikipediaListGuide(
				list_type='list_of_lists',
				wikipedia=wikipedia, echo=progress_bar - 1, data_type=CONCEPT, categories=[CONCEPT, LANGUAGE],
				urls=[
					'https://en.wikipedia.org/wiki/Lists_of_languages',
					'https://en.wikipedia.org/wiki/Lists_of_endangered_languages'
				],
				exclude_urls=[
					'https://en.wikipedia.org/wiki/List_of_ISO_639-5_codes',
					'https://en.wikipedia.org/wiki/List_of_ISO_639-3_codes',
					'https://en.wikipedia.org/wiki/IETF_language_tag',
					'https://en.wikipedia.org/wiki/Glottolog',
					'https://en.wikipedia.org/wiki/Linguasphere_Observatory',
					'https://en.wikipedia.org/wiki/SIL_International',
					'https://en.wikipedia.org/wiki/International_Organization_for_Standardization',
					'https://en.wikipedia.org/wiki/Index_of_language_articles',
					'https://en.wikipedia.org/wiki/Languages_of_East_Asia',
					'https://en.wikipedia.org/wiki/Languages_of_South_Asia',
					'https://en.wikipedia.org/wiki/List_of_revived_languages',
					'https://en.wikipedia.org/wiki/List_of_lingua_francas'
	
				],
				columns={CONCEPT: [
					'iso_language_name', 'language_name', 'language', 'official_language', 'regional_language',
					'minority_language', 'national_language', 'languages', 'name_of_macrolanguage'
				]}
			),
			'extinct_languages': WikipediaListGuide(
				list_type='list_of_lists',
				wikipedia=wikipedia, echo=progress_bar - 1, data_type=CONCEPT,
				categories=[CONCEPT, LANGUAGE, 'extinct_language', 'extinct'],
				urls=['https://en.wikipedia.org/wiki/Lists_of_extinct_languages'],
				columns={'concept': ['language']}
			),
			'languages_by_country': WikipediaListGuide(
				list_type='list',
				wikipedia=wikipedia, echo=progress_bar - 1, data_type=CONCEPT, categories=[CONCEPT, LANGUAGE],
				urls=[
					'https://en.wikipedia.org/wiki/List_of_official_languages_by_country_and_territory',
					'https://en.wikipedia.org/wiki/Afroasiatic_languages',
					'https://en.wikipedia.org/wiki/List_of_major_and_official_Austronesian_languages',
					'https://en.wikipedia.org/wiki/List_of_Indo-European_languages',
					'https://en.wikipedia.org/wiki/List_of_Mongolic_languages',
					'https://en.wikipedia.org/wiki/Tungusic_languages',
					'https://en.wikipedia.org/wiki/List_of_Turkic_languages',
					'https://en.wikipedia.org/wiki/List_of_Uralic_languages',
					'https://en.wikipedia.org/wiki/List_of_languages_by_first_written_accounts',
					'https://en.wikipedia.org/wiki/Languages_of_Afghanistan',
					'https://en.wikipedia.org/wiki/Languages_of_Bangladesh',
					'https://en.wikipedia.org/wiki/Languages_of_India',
					'https://en.wikipedia.org/wiki/Languages_with_official_status_in_India',
					'https://en.wikipedia.org/wiki/List_of_languages_by_number_of_native_speakers_in_India',
					'https://en.wikipedia.org/wiki/Languages_of_Nepal',
					'https://en.wikipedia.org/wiki/Languages_of_Pakistan'
	
				],
				columns={CONCEPT: [
					'language', 'official_language', 'regional_language', 'minority_language', 'national_language',
					'name'
				]}
			),
			'religions': WikipediaListGuide(
				list_type='list',
				wikipedia=wikipedia, echo=progress_bar - 1, data_type=CONCEPT,
				categories=[CONCEPT, 'religion'],
				urls=['https://en.wikipedia.org/wiki/List_of_religions_and_spiritual_traditions'],
				representation='list'
			),
			'religions_by_founders': WikipediaListGuide(
				list_type='list',
				wikipedia=wikipedia, echo=progress_bar - 1, data_type=CONCEPT,
				categories=[CONCEPT, 'religion'],
				urls=['https://en.wikipedia.org/wiki/List_of_founders_of_religious_traditions'],
				representation='table', columns={'religion': ['religious_tradition_founded']}
			),
			'shapes': WikipediaListGuide(
				list_type='list',
				wikipedia=wikipedia, echo=progress_bar - 1, categories=[CONCEPT, 'mathematical_concept', 'shape'],
				data_type=CONCEPT,
				urls='https://en.wikipedia.org/wiki/Lists_of_shapes',
				representation='list',
				sections=['mathematics']
			),
			'chemical_elements': WikipediaListGuide(
				list_type='list',
				wikipedia=wikipedia, echo=progress_bar - 1, data_type=CONCEPT, categories=[CONCEPT, 'chemical_concept', 'chemical_element'],
				urls='https://en.wikipedia.org/wiki/List_of_chemical_elements',
				columns={CONCEPT: ['element']}
			),
			'colors': WikipediaListGuide(
				list_type='list_of_lists',
				wikipedia=wikipedia, echo=progress_bar - 1, data_type=CONCEPT, categories=[CONCEPT, 'colour'],
				urls='https://en.wikipedia.org/wiki/Lists_of_colors',
				exclude_urls=[
					'https://en.wikipedia.org/wiki/List_of_colors_(compact)',
					'https://en.wikipedia.org/wiki/List_of_colors_by_shade',
					'https://en.wikipedia.org/wiki/List_of_color_palettes',
					'https://en.wikipedia.org/wiki/List_of_fictional_colors'
				],
				columns={CONCEPT: ['name']}
			),
			'mathematics_topics': WikipediaListGuide(
				list_type='list_of_lists',
				wikipedia=wikipedia, echo=progress_bar - 1, data_type=CONCEPT,
				categories=[CONCEPT, 'mathematics_topic'],
				urls='https://en.wikipedia.org/wiki/Lists_of_mathematics_topics',
				representation='list'
			),
			'political_science_topics': WikipediaListGuide(
				list_type='list',
				wikipedia=wikipedia, echo=progress_bar - 1, data_type=CONCEPT,
				categories=[CONCEPT, 'political_science_topic'],
				urls='https://en.wikipedia.org/wiki/Outline_of_political_science',
				representation='list',
				sections=[
					'Fields of study', 'Political theory', 'Elections', 'Political strategies', 'Political corruption',
					'Government', 'Political philosophies', 'Political issues'
				]
			),
			'time_periods': WikipediaListGuide(
				list_type='list',
				wikipedia=wikipedia, echo=progress_bar - 1, data_type=CONCEPT,
				categories=[CONCEPT, 'history_topic', 'time_period'],
				urls='https://en.wikipedia.org/wiki/List_of_time_periods',
				representation='list'
			),
			'scientific_laws': WikipediaListGuide(
				list_type='list',
				wikipedia=wikipedia, echo=progress_bar - 1, data_type=CONCEPT,
				categories=[CONCEPT, 'scientific_law'],
				urls='https://en.wikipedia.org/wiki/List_of_scientific_laws_named_after_people',
				representation='table',
				columns={CONCEPT: ['law']}
			),
			'branches_of_science': WikipediaListGuide(
				list_type='list',
				wikipedia=wikipedia, echo=progress_bar - 1, data_type=CONCEPT,
				categories=[CONCEPT, 'branch_of_science'],
				urls='https://en.wikipedia.org/wiki/Index_of_branches_of_science',
				representation='list'
			),
			'academic_disciplines': WikipediaListGuide(
				list_type='list',
				wikipedia=wikipedia, echo=progress_bar - 1, data_type=CONCEPT,
				categories=[CONCEPT, 'academic_discipline'],
				urls=[
					'https://en.wikipedia.org/wiki/Outline_of_academic_disciplines',
					'https://en.wikipedia.org/wiki/List_of_academic_fields'
				],
				representation='list'
			),
			'measurement_units': WikipediaListGuide(
				list_type='list',
				wikipedia=wikipedia, echo=progress_bar - 1, data_type=CONCEPT,
				categories=[CONCEPT, 'scientific_concept', 'measurement_unit'],
				urls='https://en.wikipedia.org/wiki/List_of_scientific_units_named_after_people',
				representation='list'
			),
			'scientific_constants': WikipediaListGuide(
				list_type='list',
				wikipedia=wikipedia, echo=progress_bar - 1, data_type=CONCEPT,
				categories=[CONCEPT, 'scientific_concept', 'scientific_constant'],
				urls='https://en.wikipedia.org/wiki/List_of_scientific_constants_named_after_people',
				representation='list'
			),
			'scientific_phenomena': WikipediaListGuide(
				list_type='list',
				wikipedia=wikipedia, echo=progress_bar - 1, data_type=CONCEPT,
				categories=[CONCEPT, 'scientific_concept', 'scientific_phenomenon'],
				urls='https://en.wikipedia.org/wiki/Scientific_phenomena_named_after_people',
				representation='list'
			),
	
		}
	)




