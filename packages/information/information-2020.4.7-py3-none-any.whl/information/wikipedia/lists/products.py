from ..WikipediaListGuide import WikipediaListGuide
from ..WikipediaLists import WikipediaLists
from chronometry.progress import ProgressBar

PRODUCT = 'product'


def get_products(wikipedia=None, echo=0):
	echo = max(0, echo)
	progress_bar = ProgressBar(echo=echo, total=None)
	return WikipediaLists(wikipedia_lists={
		'books': WikipediaListGuide(
			list_type='list_of_lists',
			wikipedia=wikipedia, echo=progress_bar - 1, data_type=PRODUCT,
			categories=[PRODUCT, 'book'],
			urls='https://en.wikipedia.org/wiki/Lists_of_books',
			columns={PRODUCT: ['title', 'book_title']},
			sections=['General lists', 'Writer lists', 'Series lists'],
			representation=None
		),
		'drugs': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=progress_bar - 1, data_type=PRODUCT,
			categories=[PRODUCT, 'drug'],
			urls='https://en.wikipedia.org/wiki/List_of_drugs_by_year_of_discovery',
			columns={PRODUCT: ['name_of_the_drug']},
			representation='table'
		),
		'software': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=progress_bar - 1, data_type=PRODUCT,
			categories=[PRODUCT, 'intangible_good', 'software', 'web_browser'],
			urls='https://en.wikipedia.org/wiki/List_of_web_browsers',
			columns={PRODUCT: ['browser', 'web_browsers']},
			sections=['Historical', 'Graphical', 'Text-based']
		),
		'programming_languages': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=progress_bar - 1, data_type=PRODUCT,
			categories=[PRODUCT, 'intangible_good', 'programming_language'],
			urls='https://en.wikipedia.org/wiki/List_of_programming_languages',
			representation='list'
		),
		'video_games': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=progress_bar - 1, data_type=PRODUCT,
			categories=[PRODUCT, 'intangible_good', 'video_game'],
			urls=[
				'https://en.wikipedia.org/wiki/List_of_video_games_considered_the_best',
				'https://en.wikipedia.org/wiki/List_of_Xbox_games',
				'https://en.wikipedia.org/wiki/List_of_Xbox_360_games',
				'https://en.wikipedia.org/wiki/List_of_PC_games',
				'https://en.wikipedia.org/wiki/List_of_grand_strategy_video_games',
				'https://en.wikipedia.org/wiki/List_of_city-building_video_games',
				'https://en.wikipedia.org/wiki/List_of_business_simulation_video_games',
				'https://en.wikipedia.org/wiki/List_of_real-time_strategy_video_games',
				'https://en.wikipedia.org/wiki/List_of_god_video_games',
				'https://en.wikipedia.org/wiki/List_of_first-person_shooters',
				'https://en.wikipedia.org/wiki/List_of_driving_and_racing_video_games',
				'https://en.wikipedia.org/wiki/List_of_roguelikes',
				'https://en.wikipedia.org/wiki/List_of_space_flight_simulator_games',
				'https://en.wikipedia.org/wiki/List_of_Macintosh_games',
				'https://en.wikipedia.org/wiki/List_of_4X_video_games',
				'https://en.wikipedia.org/wiki/List_of_games_using_Havok',
				'https://en.wikipedia.org/wiki/List_of_zombie_video_games',
				'https://en.wikipedia.org/wiki/List_of_third-person_shooters',
				'https://en.wikipedia.org/wiki/List_of_music_video_games',
				'https://en.wikipedia.org/wiki/List_of_artillery_video_games',
				'https://en.wikipedia.org/wiki/List_of_BattleTech_games',
				'https://en.wikipedia.org/wiki/List_of_turn-based_strategy_video_games',
				'https://en.wikipedia.org/wiki/List_of_real-time_tactics_video_games',
				'https://en.wikipedia.org/wiki/List_of_massively_multiplayer_online_strategy_video_games',
				'https://en.wikipedia.org/wiki/List_of_turn-based_tactics_video_games',
				'https://en.wikipedia.org/wiki/List_of_PlayStation_4_games'
			],
			columns={PRODUCT: ['game', 'title', 'title_and_source']},
			sections=['List']
		),
		'more_video_games': WikipediaListGuide(
			list_type='list_of_lists',
			wikipedia=wikipedia, echo=progress_bar - 1, categories=[PRODUCT, 'intangible_good', 'video_game'],
			data_type=PRODUCT,
			urls=[
				'https://en.wikipedia.org/wiki/Lists_of_PlayStation_3_games',
				'https://en.wikipedia.org/wiki/Lists_of_Nintendo_games'
			],
			columns={PRODUCT: ['game', 'title', 'title_and_source', 'original_title']}
		),
		'consumer_electronics': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=progress_bar - 1, categories=[PRODUCT, 'consumer_electronic'], data_type=PRODUCT,
			urls=[
				'https://en.wikipedia.org/wiki/Timeline_of_Apple_Inc._products'
			],
			columns={PRODUCT: ['model']}
		),
		'beatles_songs': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=progress_bar - 1, data_type=PRODUCT,
			categories=[PRODUCT, 'intangible_good', 'music', 'song', 'by_the_beatles'],
			urls='https://en.wikipedia.org/wiki/List_of_songs_recorded_by_the_Beatles',
			columns={PRODUCT: ['song']}
		),
		'beatles_albums': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=progress_bar - 1, data_type=PRODUCT,
			categories=[PRODUCT, 'intangible_good', 'music', 'music_album', 'by_the_beatles'],
			urls='https://en.wikipedia.org/wiki/List_of_songs_recorded_by_the_Beatles',
			columns={PRODUCT: ['core_catalogue_release', 'release_s']}
		),
		'tv_programs': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=progress_bar - 1, categories=[PRODUCT, 'intangible_good', 'tv_program'],
			data_type=PRODUCT,
			urls=[
				'https://en.wikipedia.org/wiki/List_of_television_programmes_broadcast_by_the_BBC',
				'https://en.wikipedia.org/wiki/List_of_British_television_programmes',
				'https://en.wikipedia.org/wiki/List_of_programs_broadcast_by_HBO',
				'https://en.wikipedia.org/wiki/List_of_programs_broadcast_by_GMA_Network',
				'https://en.wikipedia.org/wiki/List_of_programs_broadcast_by_ABS-CBN'
			],
			columns={PRODUCT: ['title']}
		),
		'movies': WikipediaListGuide(
			list_type='list_of_lists',
			wikipedia=wikipedia, echo=progress_bar - 1, categories=[PRODUCT, 'intangible_good', 'movie'], data_type=PRODUCT,
			urls=[
				'https://en.wikipedia.org/wiki/Lists_of_films',
				'https://en.wikipedia.org/wiki/Lists_of_anime'
			], sections=['Alphabetical indices', 'By year'],
			columns={PRODUCT: ['title', 'english_name']}
		),
		'indian_movies': WikipediaListGuide(
			list_type='list_of_lists',
			wikipedia=wikipedia, echo=progress_bar - 1,
			categories=[PRODUCT, 'intangible_good', 'movie', 'bollywood_movie', 'indian'], data_type=PRODUCT,
			urls=[
				'https://en.wikipedia.org/wiki/Lists_of_Bollywood_films'
			], sections=['Alphabetical indices', 'By year'],
			columns={PRODUCT: ['title', 'english_name']}
		),
		'american_movies': WikipediaListGuide(
			list_type='list_of_lists',
			wikipedia=wikipedia, echo=progress_bar - 1,
			categories=[PRODUCT, 'intangible_good', 'movie', 'american_movie', 'american'],
			data_type=PRODUCT,
			urls='https://en.wikipedia.org/wiki/Lists_of_American_films',
			columns={PRODUCT: ['title']}
		),
		'medicines': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=progress_bar - 1, categories=[PRODUCT, 'tangible_good', 'medicine'],
			data_type=PRODUCT,
			urls='https://en.wikipedia.org/wiki/WHO_Model_List_of_Essential_Medicines',
			representation='list'
		),
		'journals': WikipediaListGuide(
		list_type='list_of_lists',
			wikipedia=wikipedia, echo=progress_bar - 1, data_type=PRODUCT, categories=[PRODUCT, 'journal'],
			urls=[
				'https://en.wikipedia.org/wiki/List_of_journals',
				'https://en.wikipedia.org/wiki/Lists_of_academic_journals'
			],
			exclude_urls=[
				'https://en.wikipedia.org/wiki/Lists_of_academic_journals',
				'https://en.wikipedia.org/wiki/Slavic_studies',
				'https://en.wikipedia.org/wiki/Arachnology'
			],
			columns={PRODUCT: ['journal', 'journal_name', 'name', 'title']}
		),
		'websites': WikipediaListGuide(
		list_type='list_of_lists',
			wikipedia=wikipedia, echo=progress_bar - 1, data_type=PRODUCT,
			categories=[PRODUCT, 'intangible_good', 'website'],
			urls=[
				'https://en.wikipedia.org/wiki/Lists_of_websites',
				'https://en.wikipedia.org/wiki/List_of_search_engines'
			],
			exclude_urls=[
				'https://en.wikipedia.org/wiki/Lists_of_webcomics',
				'https://en.wikipedia.org/wiki/Health_information_on_the_Internet',
				'https://en.wikipedia.org/wiki/List_of_websites_blocked_in_Russia'
			],
			columns={PRODUCT: ['site', 'name', 'blog', 'website', 'site_name']}
		),
		'social_networking_websites': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=progress_bar - 1, data_type=PRODUCT,
			categories=[PRODUCT, 'intangible_good', 'website'],
			urls='https://en.wikipedia.org/wiki/List_of_social_networking_websites',
			columns={PRODUCT: ['name']}
		),
		'foods': WikipediaListGuide(
			list_type='list_of_lists',
			wikipedia=wikipedia, echo=progress_bar - 1, data_type=PRODUCT,
			categories=[PRODUCT, 'tangible_good', 'food'],
			urls=[
				'https://en.wikipedia.org/wiki/Lists_of_foods'
			],
			representation='list'
		)
	})
