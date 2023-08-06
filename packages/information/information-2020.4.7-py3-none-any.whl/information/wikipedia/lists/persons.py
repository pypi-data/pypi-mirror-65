from ..WikipediaListGuide import WikipediaListGuide
from ..WikipediaLists import WikipediaLists

from chronometry.progress import ProgressBar


PERSON = 'person'
POLITICIAN = 'politician'
PRIME_MINISTER = 'prime_minister'
MONARCH = 'monarch'
MUSICIAN = 'musician'
ARTIST = 'artist'
ATHLETE = 'athlete'

def get_person_list_guides(wikipedia=None, echo=0):
	result = {
		'religion_founders': WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, 'religion_founder'],
			urls=[
				'https://en.wikipedia.org/wiki/List_of_founders_of_religious_traditions'
			],
			representation='table',
			columns={'person': ['name']}
		),
		'female_models': WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, 'model'],
			urls=[
				'https://en.wikipedia.org/wiki/Category:American_female_models'
			],
			representation='list'
		),
		'tv_presenters': WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, 'tv_presenter'],
			urls='https://en.wikipedia.org/wiki/List_of_television_presenters',
			representation='list'
		),
		'youtubers': WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, 'youtuber'],
			urls='https://en.wikipedia.org/wiki/List_of_YouTubers',
			columns={PERSON: ['user']}
		),
		'writers': WikipediaListGuide(
			list_type='list_of_lists', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, 'writer'],
			urls=[
				'https://en.wikipedia.org/wiki/Lists_of_writers'
			],
			columns={PERSON: ['name', 'author']},
			exclude_urls=['https://en.wikipedia.org/wiki/Category:Self-help_books']
		),
		'essayists': WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, 'essayist'],
			urls='https://en.wikipedia.org/wiki/List_of_essayists',
			columns={PERSON: 'name'}
		),
		'american_writers': WikipediaListGuide(
			list_type='list_of_lists', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, 'writer', 'american'],
			urls=[
				'https://en.wikipedia.org/wiki/Lists_of_American_writers'
			],
			columns={PERSON: ['name', 'author']},
			exclude_urls=['https://en.wikipedia.org/wiki/Category:Self-help_books']
		),
		'novelists_by_century': WikipediaListGuide(
			list_type='list_of_lists', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, 'writer', 'australian'],
			urls=[
				'https://en.wikipedia.org/wiki/Category:Australian_novelists_by_century',
				'https://en.wikipedia.org/wiki/Category:Australian_writers_by_genre'
			],
			columns={PERSON: ['name', 'author']},
			exclude_urls=['https://en.wikipedia.org/wiki/Category:Self-help_books']
		),
		'english_writers': WikipediaListGuide(
			list_type='list_of_lists', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, 'writer', 'english'],
			urls=[
				'https://en.wikipedia.org/wiki/List_of_English_writers'
			],
			columns={PERSON: ['name', 'author']},
			exclude_urls=['https://en.wikipedia.org/wiki/Category:Self-help_books']
		),
		'slovak_authors': WikipediaListGuide(
			list_type='list_of_lists', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, 'writer', 'slovak'],
			urls=[
				'https://en.wikipedia.org/wiki/Lists_of_Slovak_authors'
			],
			columns={PERSON: ['name', 'author']},
			exclude_urls=['https://en.wikipedia.org/wiki/Category:Self-help_books']
		),
		'sailors': WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, 'sailor'],
			urls='https://en.wikipedia.org/wiki/List_of_sailors',
			representation='list'
		),
		'sea_captains': WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, 'sailor', 'sea_captain'],
			urls='https://en.wikipedia.org/wiki/List_of_sea_captains',
			columns={PERSON: ['about']}
		),
		'pirates': WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, 'sailor', 'pirate'],
			urls='https://en.wikipedia.org/wiki/List_of_pirates',
			columns={PERSON: ['name']}
		),
		'spies_by_nationality': WikipediaListGuide(
			list_type='list_of_lists', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, 'spy'],
			urls='https://en.wikipedia.org/wiki/Category:Spies_by_nationality',
			representation='list'
		),
		'american_spies': WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, 'spy', 'american'],
			urls=[
				'https://en.wikipedia.org/wiki/List_of_American_spies',
			],
			columns={PERSON: 'person'}
		),
		'british_spies': WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, 'spy', 'british'],
			urls=[
				'https://en.wikipedia.org/wiki/List_of_British_spies',
			],
			columns={PERSON: 'person'}
		),
		'spies_in_world_war_ii': WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, 'spy', 'world_war_2'],
			urls=[
				'https://en.wikipedia.org/wiki/List_of_spies_in_World_War_II'
			],
			columns={PERSON: 'person'}
		),
		'astronauts_by_name': WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, 'astronaut'],
			urls=[
				'https://en.wikipedia.org/wiki/List_of_astronauts_by_name'
			],
			representation='list'
		),
		'chief_executive_officers': WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, 'executive', 'ceo'],
			urls='https://en.wikipedia.org/wiki/List_of_chief_executive_officers',
			columns={PERSON: 'executive'}
		),
		'chief_financial_officers': WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, 'executive', 'cfo'],
			urls='https://en.wikipedia.org/wiki/Category:Chief_financial_officers',
			sections=['Pages in category'],
			representation='list'
		),
		'jewish_american_businesspeople': WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, 'business_person', 'jewish', 'american'],
			urls='https://en.wikipedia.org/wiki/List_of_Jewish_American_businesspeople',
			representation='list'
		),
		'physicists': WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, 'scientist', 'physicist'],
			urls='https://en.wikipedia.org/wiki/List_of_physicists',
			representation='list'
		),
		'mathematicians': WikipediaListGuide(
			list_type='list_of_lists', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, 'scientist', 'mathematician'],
			urls='https://en.wikipedia.org/wiki/Lists_of_mathematicians',
			representation='list'
		),
		'chemists': WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, 'scientist', 'chemist'],
			urls='https://en.wikipedia.org/wiki/List_of_chemists',
			representation='list'
		),
		'economists': WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, 'scientist', 'economist'],
			urls='https://en.wikipedia.org/wiki/List_of_economists',
			representation='list'
		),
		'data_scientists': WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, 'scientist', 'data_scientist'],
			urls='https://en.wikipedia.org/wiki/Category:Data_scientists',
			representation='list',
			sections='Pages in category'
		),
		'computer_scientists': WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, 'scientist', 'computer_scientist'],
			urls=[
				'https://en.wikipedia.org/wiki/List_of_computer_scientists',
				'https://en.wikipedia.org/wiki/List_of_pioneers_in_computer_science'
			],
			columns={PERSON: 'person'}
		),
		'programmers': WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, 'programmer'],
			urls='https://en.wikipedia.org/wiki/List_of_programmers',
			representation='list'
		),
		'astronomers': WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, 'scientist', 'astronomer'],
			urls='https://en.wikipedia.org/wiki/List_of_astronomers',
			representation='list'
		),
		'philosophers': WikipediaListGuide(
			list_type='list_of_lists', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, 'philosopher'],
			urls='https://en.wikipedia.org/wiki/Lists_of_philosophers',
			exclude_urls=[
				'https://en.wikipedia.org/wiki/Christian_philosophy',
				'https://en.wikipedia.org/wiki/Continental_philosophy',
				'https://en.wikipedia.org/wiki/Index_of_Eastern_philosophy_articles',
				'https://en.wikipedia.org/wiki/Anarchism',
				'https://en.wikipedia.org/wiki/Pragmatism',
				'https://en.wikipedia.org/wiki/List_of_Armenian_scientists',
				'https://en.wikipedia.org/wiki/List_of_people_from_the_Basque_Country',
				'https://en.wikipedia.org/wiki/List_of_Jewish_scientists'
			],
			columns={PERSON: ['name']}
		),
		'serial_killers': WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, 'serial_killer'],
				urls=[
				'https://en.wikipedia.org/wiki/List_of_serial_killers_by_number_of_victims',
				'https://en.wikipedia.org/wiki/List_of_serial_killers_by_country',
				'https://en.wikipedia.org/wiki/List_of_serial_killers_in_the_United_States',
				'https://en.wikipedia.org/wiki/List_of_serial_killers_before_1900'
			],
			columns={PERSON: 'name'}
		),
		'richest_people': WikipediaListGuide(
			list_type='list_of_lists', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, 'richest_in_the_world'],
				urls='https://en.wikipedia.org/wiki/Lists_of_people_by_net_worth',
			sections = ['By nationality', 'By region'],
			columns={PERSON: ['name']}
		),
		'prime_ministers_of_the_united_kingdom': WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, POLITICIAN, PRIME_MINISTER, 'british'],
			urls='https://en.wikipedia.org/wiki/List_of_Prime_Ministers_of_the_United_Kingdom_by_tenure',
			representation='table',
			columns={PERSON: ['prime_minister']}
		),
		'prime_ministers_of_canada': WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, POLITICIAN, PRIME_MINISTER, 'canadian'],
			urls='https://en.wikipedia.org/wiki/List_of_Prime_Ministers_of_Canada',
			representation='table',
			columns={PERSON: ['name']}
		),
		'presidents_of_the_philippines': WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, POLITICIAN, 'president', 'filipino'],
			urls='https://en.wikipedia.org/wiki/List_of_Presidents_of_the_Philippines',
			columns={PERSON: ['name']}
		),
		'presidents_of_the_united_states': WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, POLITICIAN, 'president', 'american'],
			urls=[
				'https://en.wikipedia.org/wiki/List_of_Presidents_of_the_United_States_by_previous_experience',
				'https://en.wikipedia.org/wiki/List_of_Presidents_of_the_United_States_by_home_state'
			],
			representation='table',
			columns={PERSON: ['president_2', 'president']}
		),
		'members_of_the_united_states_congress': WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, POLITICIAN, 'member_of_congress', 'american'],
			urls='https://en.wikipedia.org/wiki/List_of_members_of_the_United_States_Congress_by_longevity_of_service',
			columns={PERSON: 'name'}
		),
		'vice_presidents_of_the_united_states': WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, POLITICIAN, 'vice_president', 'american'],
			urls='https://en.wikipedia.org/wiki/List_of_Vice_Presidents_of_the_United_States',
			columns={PERSON: 'vice_president'}
		),
		'united_states_senators': WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, POLITICIAN, 'senator', 'american'],
			urls='https://en.wikipedia.org/wiki/List_of_current_United_States_Senators',
			columns={PERSON: ['officer', 'senator']}
		),
		'justices_of_the_supreme_court_of_the_united_states': WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, POLITICIAN, 'justice', 'supreme_court_justice', 'american'],
			urls='https://en.wikipedia.org/wiki/List_of_Justices_of_the_Supreme_Court_of_the_United_States',
			columns={PERSON: ['justice']}
		),
		'members_of_the_united_states_house_of_representatives': WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, POLITICIAN, 'member_of_parliament', 'american'],
			urls='https://en.wikipedia.org/wiki/List_of_current_members_of_the_United_States_House_of_Representatives',
			columns={PERSON: ['officer', 'member']}
		),
		'united_states_governors': WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, POLITICIAN, 'governor', 'american'],
			urls='https://en.wikipedia.org/wiki/List_of_United_States_governors',
			columns={PERSON: 'governor'}
		),
		'chinese_leaders': WikipediaListGuide(
			list_type='list_of_lists', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, POLITICIAN, 'leader', 'chinese'],
			urls='https://en.wikipedia.org/wiki/List_of_Chinese_leaders',
			columns={PERSON: ['name']}
		),
		'indian_politicians': WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, POLITICIAN, 'indian'],
			urls=[
				'https://en.wikipedia.org/wiki/List_of_Prime_Ministers_of_India',
				'https://en.wikipedia.org/wiki/List_of_current_Indian_chief_ministers',
				'https://en.wikipedia.org/wiki/List_of_current_Indian_governors',
				'https://en.wikipedia.org/wiki/List_of_current_Indian_chief_justices',
				'https://en.wikipedia.org/wiki/List_of_current_Indian_legislative_speakers_and_chairmen',
				'https://en.wikipedia.org/wiki/List_of_current_Indian_opposition_leaders',
				'https://en.wikipedia.org/wiki/List_of_Chief_Justices_of_India',
				'https://en.wikipedia.org/wiki/List_of_sitting_judges_of_the_Supreme_Court_of_India',
				'https://en.wikipedia.org/wiki/List_of_former_judges_of_the_Supreme_Court_of_India',
				'https://en.wikipedia.org/wiki/List_of_chief_ministers_from_the_Communist_Party_of_India_(Marxist)',
				'https://en.wikipedia.org/wiki/List_of_chief_ministers_from_the_Indian_National_Congress',
				'https://en.wikipedia.org/wiki/List_of_chief_ministers_from_the_Bharatiya_Janata_Party',
				'https://en.wikipedia.org/wiki/List_of_current_Indian_deputy_chief_ministers'
			],
			columns={PERSON: ['name', 'chief_justice', 'speaker', 'opposition_leader', 'name_of_the_justice']}
		),
		'nazis': WikipediaListGuide(
			list_type='list_of_lists', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, 'nazi'],
			urls='https://en.wikipedia.org/wiki/List_of_Nazis',
			representation='list'
		),
		'gay_lesbian_or_bisexual_people': WikipediaListGuide(
			list_type='list_of_lists', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, 'lgbt_person'],
			urls='https://en.wikipedia.org/wiki/List_of_gay,_lesbian_or_bisexual_people',
			columns={PERSON: ['name']}
		),
		'persons_by_nationality': WikipediaListGuide(
			list_type='list_of_lists', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=PERSON,
			urls=[
				'https://en.wikipedia.org/wiki/Lists_of_people_by_nationality',
				'https://en.wikipedia.org/wiki/Lists_of_people_from_African_Union_states',
				'https://en.wikipedia.org/wiki/Lists_of_people_from_India_by_state',
				'https://en.wikipedia.org/wiki/Lists_of_New_Zealanders',
				'https://en.wikipedia.org/wiki/Category:New_Zealand_M%C4%81ori_people',
				'https://en.wikipedia.org/wiki/List_of_Sri_Lankan_people',
				'https://en.wikipedia.org/wiki/List_of_Swedish_people',
				'https://en.wikipedia.org/wiki/Lists_of_Indigenous_Australians',
				'https://en.wikipedia.org/wiki/Lists_of_Inuit',
				'https://en.wikipedia.org/wiki/List_of_Tamil_people'
			],
			exclude_urls=[
				'https://en.wikipedia.org/wiki/Filipinos',
				'https://en.wikipedia.org/wiki/Malagasy_people',
				'https://en.wikipedia.org/wiki/List_of_New_Zealand_child_actors',
				'https://en.wikipedia.org/wiki/Blogging_in_New_Zealand',
				'https://en.wikipedia.org/wiki/Congregation_of_Christian_Brothers_in_New_Zealand',
				'https://en.wikipedia.org/wiki/Surinamese_people',
				'https://en.wikipedia.org/wiki/Tibetan_people',
				'https://en.wikipedia.org/wiki/List_of_Huaorani_people',
				'https://en.wikipedia.org/wiki/Sindhis',
				'https://en.wikipedia.org/wiki/Category:Lists_of_fictional_Chinese_people',
				'https://en.wikipedia.org/wiki/Disciples_of_Confucius',
				'https://en.wikipedia.org/wiki/Four_Beauties',
				'https://en.wikipedia.org/wiki/Four_Lords_of_the_Warring_States',
				'https://en.wikipedia.org/wiki/Falkland_Islanders',
				'https://en.wikipedia.org/wiki/Boer',
				'https://en.wikipedia.org/wiki/Han_Chinese'

			],
			columns={PERSON: [
				'name', 'posthumous_name', 'tokugawas_2', 'prime_minister', 'member_1', 'player',
				'name_1', 'title', 'name_by_which_most_commonly_known', 'laureate_3', 'president',
				'first_lady_gentleman'
			]}
		),
		'actors': WikipediaListGuide(
			list_type='list_of_lists', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, ARTIST, 'actor'],
			urls=[
				'https://en.wikipedia.org/wiki/Lists_of_actors'
			],
			sections=['Nationality'],
			columns={PERSON: ['name', 'actor_role', 'actor', ]}
		),
		'korean_actors': WikipediaListGuide(
			list_type='list_of_lists', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, ARTIST, 'actor', 'south_korean'],
			urls=[
				'https://en.wikipedia.org/wiki/List_of_South_Korean_actors'
			],
			sections=['nationality'],
			columns={PERSON: ['name', 'actor_role', 'actor', ]}
		),
		'musicians': WikipediaListGuide(
			list_type='list_of_lists', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, ARTIST, MUSICIAN],
			urls=[
				'https://en.wikipedia.org/wiki/Lists_of_musicians'
			],
			sections=['Instrument', 'Location or nationality'],
			columns={PERSON: ['musician', 'name', 'artist_name', 'band', 'artist_s', 'artist', 'band_name']}
		),
		'fiddlers': WikipediaListGuide(
			list_type='list_of_lists', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, ARTIST, MUSICIAN, 'fiddler'],
			urls='https://en.wikipedia.org/wiki/List_of_fiddlers',
			columns={PERSON: 'name_of_fiddler'}
		)
	}

	artist_urls_and_categories = [
		('https://en.wikipedia.org/wiki/List_of_architects', ['architect']),
		('https://en.wikipedia.org/wiki/List_of_animators', ['animator']),
		('https://en.wikipedia.org/wiki/List_of_dancers', ['dancer']),
		('https://en.wikipedia.org/wiki/List_of_fashion_designers', ['fashion_designer']),
		('https://en.wikipedia.org/wiki/List_of_illustrators', ['illustrator']),
		('https://en.wikipedia.org/wiki/List_of_tattoo_artists', ['tattoo_artist']),
		('https://en.wikipedia.org/wiki/List_of_photographers', ['photographer']),
		('https://en.wikipedia.org/wiki/List_of_photojournalists', ['photojournalist', 'photographer']),
		('https://en.wikipedia.org/wiki/List_of_sculptors', ['sculptor']),
		('https://en.wikipedia.org/wiki/List_of_comedians', ['comedian']),
		('https://en.wikipedia.org/wiki/List_of_poets', ['poet']),
		('https://en.wikipedia.org/wiki/List_of_musicians_from_Chicago', ['musician', 'chicagoan']),
		('https://en.wikipedia.org/wiki/List_of_jazz_musicians', ['musician', 'jazz_musician'])
	]

	for urls, categories in artist_urls_and_categories:
		result[f'other_artists_{categories[0]}'] = WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, ARTIST] + categories,
			urls=urls,
			columns={PERSON: 'name'}
		)

	athlete_urls_and_categories = [
		('https://en.wikipedia.org/wiki/Lists_of_sportspeople', []),
		('https://en.wikipedia.org/wiki/Lists_of_Major_League_Baseball_players', ['baseball_player']),
		('https://en.wikipedia.org/wiki/Lists_of_National_Basketball_Association_players', ['basketball_player']),
		('https://en.wikipedia.org/wiki/Lists_of_American_football_players', ['american_football_player']),
		('https://en.wikipedia.org/wiki/List_of_Pro_Bowl_players', ['bowl_player']),
		('https://en.wikipedia.org/wiki/Lists_of_association_football_players', ['association_football_player']),
		('https://en.wikipedia.org/wiki/Lists_of_golfers', ['golfer']),
		('https://en.wikipedia.org/wiki/List_of_NHL_players', ['hockey_player']),
		('https://en.wikipedia.org/wiki/Lists_of_kickboxers', ['kickboxer']),
		('https://en.wikipedia.org/wiki/Category:Lists_of_rowers', ['rower']),
		('https://en.wikipedia.org/wiki/Category:Lists_of_skiers', ['skier']),
		('https://en.wikipedia.org/wiki/Category:Lists_of_female_skiers', ['skier', 'female']),
		('https://en.wikipedia.org/wiki/Category:Lists_of_male_skiers', ['skier', 'male']),
		('https://en.wikipedia.org/wiki/Category:Lists_of_alpine_skiers', ['skier']),
		('https://en.wikipedia.org/wiki/Category:Lists_of_ski_jumping_medalists', ['ski_jumper']),
		('https://en.wikipedia.org/wiki/Category:Racing_drivers_by_competition', ['racing_driver']),
		('https://en.wikipedia.org/wiki/Lists_of_tennis_players', ['tennis_player']),
		('https://en.wikipedia.org/wiki/Lists_of_wrestlers', ['wrestler']),
		('https://en.wikipedia.org/wiki/List_of_Formula_One_World_Drivers%27_Champions', ['racing_driver'])
	]

	for urls, categories in athlete_urls_and_categories:
		category = categories[0] if len(categories) > 0 else ''
		result[f'other_athletes_{category}'] = WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, ATHLETE] + categories,
			urls=urls,
			columns={PERSON: [
				'player', 'son_s', 'name', 'women', 'men', 'skater', 'gold', 'silver', 'bronze',
				'1st', '2nd', '3rd', 'winner', 'runner_up', 'third', 'singles_men', 'singles_women',
				'doubles_men', 'doubles_women', 'doubles_mixed', 'driver'
			]}
		)

	monarchs_dictionary = {
		'english': 'https://en.wikipedia.org/wiki/List_of_English_monarchs',
		'russian': 'https://en.wikipedia.org/wiki/List_of_Russian_monarchs',
		'polish': 'https://en.wikipedia.org/wiki/List_of_Polish_monarchs',
		'swedish': 'https://en.wikipedia.org/wiki/List_of_Swedish_monarchs',
		'ottoman': 'https://en.wikipedia.org/wiki/List_of_sultans_of_the_Ottoman_Empire',
		'saudi': 'https://en.wikipedia.org/wiki/King_of_Saudi_Arabia',
		'portuguese': 'https://en.wikipedia.org/wiki/List_of_Portuguese_monarchs'
	}

	for nationality, url in monarchs_dictionary.items():
		result[f'{nationality}_{MONARCH}s'] = WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, MONARCH, nationality, f'{nationality}_monarch'],
			columns={PERSON: ['name', 'sultan']}, urls=url
		)

	others_dictionary = {
		'freemason': [
			'https://en.wikipedia.org/wiki/List_of_Freemasons_(A%E2%80%93D)',
			'https://en.wikipedia.org/wiki/List_of_Freemasons_(E%E2%80%93Z)'
		],
		'atheist': [
			'https://en.wikipedia.org/wiki/List_of_atheists_in_science_and_technology',
			'https://en.wikipedia.org/wiki/List_of_atheist_authors',
			'https://en.wikipedia.org/wiki/List_of_atheist_philosophers'
		],
		'died_in_traffic_collision': 'https://en.wikipedia.org/wiki/List_of_people_who_died_in_traffic_collisions',
		'nobel_laureate': 'https://en.wikipedia.org/wiki/List_of_Nobel_laureates',
		'porn_star': 'https://en.wikipedia.org/wiki/List_of_pornographic_performers_by_decade',
		'leader_of_soviet_union': 'https://en.wikipedia.org/wiki/List_of_leaders_of_the_Soviet_Union'
	}

	for category, urls in others_dictionary.items():
		result[category] = WikipediaListGuide(
			list_type='list', data_type=PERSON, echo=echo - 1,
			wikipedia=wikipedia, categories=[PERSON, category], urls=urls,
			columns={PERSON: [
				'name', 'physics', 'chemistry', 'physiology_or_medicine', 'literature', 'peace', 'economics',
				'name_lifetime'
			]}
		)

	return result


def get_persons(wikipedia=None, echo=0):
	echo = max(0, echo)
	progress_bar = ProgressBar(echo=echo, total=None)
	list_guides = get_person_list_guides(wikipedia=wikipedia, echo=progress_bar)
	return WikipediaLists(wikipedia_lists=list_guides, categories=[PERSON], echo=progress_bar)