from ..WikipediaListGuide import WikipediaListGuide
from ..WikipediaLists import WikipediaLists
from chronometry.progress import ProgressBar

ORGANIZATION = 'organization'


def get_ngo_guides(wikipedia=None, echo=0):

	urls_and_categories = [
		('https://en.wikipedia.org/wiki/Category:Non-governmental_organizations', []),
		('https://en.wikipedia.org/wiki/Category:Anti-corruption_non-governmental_organizations', ['anti_corruption']),
		('https://en.wikipedia.org/wiki/Category:International_nongovernmental_organizations', ['international']),
		(
			'https://en.wikipedia.org/wiki/Category:Non-governmental_organizations_involved_in_the_Israeli%E2%80%93Palestinian_conflict',
			['involved_in_israel_palestine_conflict']
		),
		(
			'https://en.wikipedia.org/wiki/Category:Non-governmental_organizations_involved_in_the_Israeli%E2%80%93Palestinian_peace_process',
			['involved_in_israel_palestine_conflict']
		),
		(
			'https://en.wikipedia.org/wiki/Category:Non-governmental_organizations_involved_in_the_Israeli%E2%80%93Syrian_conflict',
			['involved_in_israel_syria_conflict']
		),
		(
			'https://en.wikipedia.org/wiki/Category:Non-governmental_organizations_involved_in_the_Turkish_War_of_Independence',
			['involved_in_turkish_war_of_independence']
		),
		(
			'https://en.wikipedia.org/wiki/Category:Non-governmental_organizations_with_consultative_status_at_the_United_Nations',
			['united_nations_consultative_ngo']
		),
		('https://en.wikipedia.org/wiki/Category:World_War_II_non-governmental_organizations', ['world_war_2_ngo']),
		('https://en.wikipedia.org/wiki/Category:Non-governmental_organization_stubs', ['ngo_stub']),
		('https://en.wikipedia.org/wiki/International_non-governmental_organization', ['international']),
		('https://en.wikipedia.org/wiki/List_of_non-governmental_organisations_in_India', ['india']),
		('https://en.wikipedia.org/wiki/List_of_non-governmental_organizations_in_China', ['china']),
		('https://en.wikipedia.org/wiki/List_of_human_rights_organisations', ['human_rights_ngo']),
		('https://en.wikipedia.org/wiki/List_of_environmental_organizations', ['environmental_ngo']),
		('https://en.wikipedia.org/wiki/List_of_non-governmental_organizations_in_Pakistan', ['pakistan']),
		('https://en.wikipedia.org/wiki/List_of_non-governmental_organisations_in_Bangladesh', ['bangladesh']),
		(
			'https://en.wikipedia.org/wiki/List_of_non-governmental_organisations_based_in_Karachi',
			['pakistan', 'karachi']
		),
		('https://en.wikipedia.org/wiki/List_of_youth_organizations', ['youth_organization']),
		('https://en.wikipedia.org/wiki/List_of_non-governmental_organisations_in_Kenya', ['kenya']),
		(
			'https://en.wikipedia.org/wiki/List_of_organizations_that_combat_human_trafficking',
			['anti_human_trafficking_ngo']
		),
		('https://en.wikipedia.org/wiki/List_of_non-governmental_organizations_in_Vietnam', ['vietnam']),
		('https://en.wikipedia.org/wiki/List_of_women%27s_organizations', ['womens_organization']),
		('https://en.wikipedia.org/wiki/List_of_international_organizations_based_in_Geneva', ['switzerland', 'geneva'])
	]

	return {
		(urls[0] if isinstance(urls, list) else urls): WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=echo - 1, data_type=ORGANIZATION, categories=[ORGANIZATION, 'ngo'] + categories,
			urls=urls, sections=['Pages in category'], columns={ORGANIZATION: ['name', 'name_of_ngo']}
		)
		for urls, categories in urls_and_categories
	}


def get_charity_guides(wikipedia=None, echo=0):

	charities_urls_and_categories = [
		('https://en.wikipedia.org/wiki/List_of_charitable_foundations', []),
		('https://en.wikipedia.org/wiki/Category:Charities_based_in_Canada', ['canada']),
		(
			'https://en.wikipedia.org/wiki/Category:Charities_based_in_Washington,_D.C.',
			['united_states', 'washington_dc']
		),
		(
			'https://en.wikipedia.org/wiki/Category:Animal_charities_based_in_the_United_States',
			['united_states', 'animal_charity']
		),
		(
			'https://en.wikipedia.org/wiki/Category:Children%27s_charities_based_in_the_United_States',
			['united_states', 'children_charity']
		),
		(
			'https://en.wikipedia.org/wiki/Category:Development_charities_based_in_the_United_States',
			['united_states', 'development_charity']
		),
		(
			'https://en.wikipedia.org/wiki/Category:Educational_charities_based_in_the_United_States',
			['united_states', 'educational_charity']
		),
		('https://en.wikipedia.org/wiki/Category:Foundations_based_in_the_United_States', ['united_states']),
		(
			'https://en.wikipedia.org/wiki/Category:Health_charities_in_the_United_States',
			['united_states', 'health_charity']
		),
		(
			'https://en.wikipedia.org/wiki/Category:Prison_charities_based_in_the_United_States',
			['united_states', 'prison_charity']
		),
		(
			'https://en.wikipedia.org/wiki/Category:Religious_charities_based_in_the_United_States',
			['united_states', 'religious_charity']
		),
		(
			'https://en.wikipedia.org/wiki/Category:Social_welfare_charities_based_in_the_United_States',
			['united_states', 'social_welfare_charity']
		)
	]

	charities = {
		(urls[0] if isinstance(urls, list) else urls): WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=echo - 1,
			data_type=ORGANIZATION, categories=[ORGANIZATION, 'charity'] + categories,
			urls=urls,
			sections=['Pages in category'],
			representation='list'
		)
		for urls, categories in charities_urls_and_categories
	}

	by_continent_urls_and_categories = [
		('https://en.wikipedia.org/wiki/Category:Charities_based_in_Europe', ['europe']),
		('https://en.wikipedia.org/wiki/Category:Charities_based_in_Africa', ['africa']),
		('https://en.wikipedia.org/wiki/Category:Charities_based_in_Asia', ['asia']),
		('https://en.wikipedia.org/wiki/Category:Charities_based_in_North_America', ['north_america']),
		('https://en.wikipedia.org/wiki/Category:Charities_based_in_South_America', ['south_america'])
	]
	by_continent = {
		(urls[0] if isinstance(urls, list) else urls): WikipediaListGuide(
			list_type='list_of_lists',
			wikipedia=wikipedia, echo=echo - 1, data_type=ORGANIZATION,
			categories=[ORGANIZATION, 'charity'] + categories,
			sections=['Subcategories'], representation='list', urls=urls
		)
		for urls, categories in by_continent_urls_and_categories
	}

	return {**by_continent, **charities}


def get_univesity_guides(wikipedia=None, echo=0):

	international = WikipediaListGuide(
		list_type='list_of_lists',
		wikipedia=wikipedia, echo=echo - 1, categories=[ORGANIZATION, 'academic', 'university'], data_type=ORGANIZATION,
		urls=[
			'https://en.wikipedia.org/wiki/Lists_of_universities_and_colleges_by_country',
			'https://en.wikipedia.org/wiki/Lists_of_American_institutions_of_higher_education'
		],
		exclude_urls=[
			'https://en.wikipedia.org/wiki/Lists_of_American_institutions_of_higher_education',
			'https://en.wikipedia.org/wiki/Anton_de_Kom_University_of_Suriname',
			'https://en.wikipedia.org/wiki/List_of_universities_in_India',
			'https://en.wikipedia.org/wiki/University_of_Greenland',
			'https://en.wikipedia.org/wiki/Universitat_d%27Andorra',
			'https://en.wikipedia.org/wiki/University_of_Gibraltar',
			'https://en.wikipedia.org/wiki/List_of_universities_in_Greece',
			'https://en.wikipedia.org/wiki/University_of_Luxembourg',
			'https://en.wikipedia.org/wiki/International_University_of_Monaco',
			'https://en.wikipedia.org/wiki/List_of_schools_in_Papua_New_Guinea'
		],
		columns={ORGANIZATION: [
			'university', 'institution', 'university_name', 'name_of_university', 'school', 'name_in_english',
			'unofficial_name_in_english', 'university_full_name', 'university_college', 'institute_name', 'name',
			'universities', 'english_name'
		]}

	)
	india = WikipediaListGuide(
		list_type='list',
		wikipedia=wikipedia, echo=echo - 1, categories=[ORGANIZATION, 'academic', 'university', 'indian'], data_type=ORGANIZATION,
		urls=[
			'https://en.wikipedia.org/wiki/Institutes_of_National_Importance',
			'https://en.wikipedia.org/wiki/Central_university_(India)',
			'https://en.wikipedia.org/wiki/List_of_deemed_universities',
			'https://en.wikipedia.org/wiki/List_of_private_universities_in_India',
			'https://en.wikipedia.org/wiki/List_of_state_universities_in_India'
		],
		representation='table',
		columns={ORGANIZATION: ['university', 'institution']}
	)
	return {'international_universities': international, 'indian_universities': india}


def get_temple_guides(wikipedia=None, echo=0):

	churches = WikipediaListGuide(
		list_type='list_of_lists',
		wikipedia=wikipedia, echo=echo - 1, data_type=ORGANIZATION, categories=[ORGANIZATION, 'religious', 'church'],
		urls=[
			'https://en.wikipedia.org/wiki/Category:Lists_of_churches',
			'https://en.wikipedia.org/wiki/Lists_of_Armenian_churches',
			'https://en.wikipedia.org/wiki/Lists_of_cathedrals'
		],
		sections=['Pages in category'],
		exclude_urls=[
			'https://en.wikipedia.org/wiki/List_of_churches_in_Albania',
			'https://en.wikipedia.org/wiki/List_of_Buddhist_temples',
			'https://en.wikipedia.org/wiki/Lists_of_cathedrals',
			'https://en.wikipedia.org/wiki/List_of_churches_of_the_Jesuit_Missions_of_the_Chiquitos',
			'https://en.wikipedia.org/wiki/Friends_meeting_house',
			'https://en.wikipedia.org/wiki/Greek_Catholic_Church',
			'https://en.wikipedia.org/wiki/List_of_churches_in_North_Macedonia'
		],
		columns={ORGANIZATION: [
			'church_temple', 'name', 'church', 'cathedral_church', 'building', 'temple_name_english',
			'name_of_church'
		]}
	)
	buddhist = WikipediaListGuide(
		list_type='list',
		wikipedia=wikipedia, echo=echo - 1, data_type=ORGANIZATION, categories=[ORGANIZATION, 'religious', 'buddhist_temple'],
		urls=[
			'https://en.wikipedia.org/wiki/List_of_Buddhist_temples'
		],
		representation='list'
	)
	return {'churches': churches, 'buddhist_temples': buddhist}


def get_political_party_guides(wikipedia=None, echo=0):

	return {
		'political_parties_in_india': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=echo - 1, data_type=ORGANIZATION,
			categories=[ORGANIZATION, 'political_party', 'india'],
			urls='https://en.wikipedia.org/wiki/List_of_political_parties_in_India',
			columns={ORGANIZATION: 'name'}
		),
		'political_parties_in_the_united_kingdom': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=echo - 1, data_type=ORGANIZATION,
			categories=[ORGANIZATION, 'political_party', 'united_kingdom'],
			urls='https://en.wikipedia.org/wiki/List_of_political_parties_in_the_United_Kingdom',
			columns={ORGANIZATION: 'party'}
		),
		'political_parties_in_the_united_states': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=echo - 1, data_type=ORGANIZATION,
			categories=[ORGANIZATION, 'political_party', 'united_states'],
			urls='https://en.wikipedia.org/wiki/List_of_political_parties_in_the_United_States',
			columns={ORGANIZATION: 'party'}
		),
		'largest_political_parties': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=echo - 1, data_type=ORGANIZATION,
			categories=[ORGANIZATION, 'political_party'],
			urls='https://en.wikipedia.org/wiki/List_of_largest_political_parties',
			columns={ORGANIZATION: 'name'}
		),
		'green_political_parties': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=echo - 1, data_type=ORGANIZATION,
			categories=[ORGANIZATION, 'political_party', 'green_party'],
			urls='https://en.wikipedia.org/wiki/List_of_green_political_parties',
			representation='list'
		),
		'generic_names_of_political_parties': WikipediaListGuide(
			list_type='list_of_lists',
			wikipedia=wikipedia, echo=echo - 1, data_type=ORGANIZATION,
			categories=[ORGANIZATION, 'political_party'],
			urls='https://en.wikipedia.org/wiki/List_of_generic_names_of_political_parties',
			exclude_urls=[
				'https://en.wikipedia.org/wiki/Green_Party',
				'https://en.wikipedia.org/wiki/Industrial_Workers_of_the_World',
				'https://en.wikipedia.org/wiki/Radical_Party_of_the_Left'
			],
			columns={ORGANIZATION: ['party']}
		),
		'outlaw_motorcycle_clubs': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=echo - 1, data_type=ORGANIZATION,
			categories=[ORGANIZATION, 'outlaw', 'motorcycle_club'],
			urls='https://en.wikipedia.org/wiki/List_of_outlaw_motorcycle_clubs',
			columns={ORGANIZATION: ['name']}
		)
	}


def get_terrorist_group_guides(wikipedia=None, echo=0):

	return {'terrorist_groups': WikipediaListGuide(
		list_type='list',
		wikipedia=wikipedia, echo=echo - 1, data_type=ORGANIZATION, categories=[ORGANIZATION, 'terrorist_group'],
		urls='https://en.wikipedia.org/wiki/List_of_designated_terrorist_groups',
		columns={ORGANIZATION: 'organization'}
	)}


def get_sports_team_guides(wikipedia=None, echo=0):
	CLUB = 'sporting_club'
	return {
		'sports_teams_of_the_united_states_and_canada': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=echo - 1, data_type=ORGANIZATION, categories=[ORGANIZATION, CLUB, 'north_america'],
			urls='https://en.wikipedia.org/wiki/Major_professional_sports_teams_of_the_United_States_and_Canada',
			columns={ORGANIZATION: 'team'}, sections=['Teams']
		),
		'national_basketball_association': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=echo - 1, data_type=ORGANIZATION, categories=[ORGANIZATION, CLUB, 'basketball_team', 'nba_club'],
			urls='https://en.wikipedia.org/wiki/National_Basketball_Association',
			columns={ORGANIZATION: 'team'}, sections=['Teams']
		),
		'relocated_national_basketball_association_teams': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=echo - 1, data_type=ORGANIZATION,
			categories=[ORGANIZATION, CLUB, 'basketball_club', 'nba_club', 'relocated_club'],
			urls='https://en.wikipedia.org/wiki/List_of_relocated_National_Basketball_Association_teams',
			sections=['Relocated teams']
		),
		'association_football_club': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=echo - 1, data_type=ORGANIZATION, categories=[ORGANIZATION, 'association_football_club'],
			urls=[
				'https://en.wikipedia.org/wiki/List_of_top-division_football_clubs_in_CAF_countries',
				'https://en.wikipedia.org/wiki/List_of_top-division_football_clubs_in_AFC_countries',
				'https://en.wikipedia.org/wiki/List_of_top-division_football_clubs_in_UEFA_countries',
				'https://en.wikipedia.org/wiki/List_of_second_division_football_clubs_in_UEFA_countries',
				'https://en.wikipedia.org/wiki/List_of_top-division_football_clubs_in_CONCACAF_countries',
				'https://en.wikipedia.org/wiki/List_of_top-division_football_clubs_in_OFC_countries',
				'https://en.wikipedia.org/wiki/List_of_top-division_football_clubs_in_CONMEBOL_countries',
				'https://en.wikipedia.org/wiki/List_of_top-division_football_clubs_in_non-FIFA_countries'
			],
			columns={ORGANIZATION: ['club', 'team']}
		),
		'cricket_teams': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=echo - 1, data_type=ORGANIZATION, categories=[ORGANIZATION, 'cricket_club'],
			urls='https://en.wikipedia.org/wiki/List_of_current_first-class_cricket_teams',
			columns={ORGANIZATION: 'name'}
		)
	}


def get_intergovernmental(wikipedia=None, echo=0):

	return {'intergovernmental_organizations': WikipediaListGuide(
		list_type='list',
		wikipedia=wikipedia, echo=echo - 1, data_type=ORGANIZATION, categories=[ORGANIZATION, 'intergovernmental'],
		urls=[
			'https://en.wikipedia.org/wiki/List_of_intergovernmental_organizations'
		],
		exclude_pages=[
			'https://en.wikipedia.org/wiki/Eurasia',
			'https://en.wikipedia.org/wiki/Mediterranean_Sea',
			'https://en.wikipedia.org/wiki/Indian_Ocean',
			'https://en.wikipedia.org/wiki/Arctic_Ocean',
			'https://en.wikipedia.org/wiki/Pacific_Ocean',
			'https://en.wikipedia.org/wiki/African,_Caribbean_and_Pacific_Group_of_States'
		],
		representation='list'
	)}


def get_organizations(wikipedia=None, echo=0):
	echo = max(0, echo)
	progress_bar = ProgressBar(echo=echo, total=None)
	return WikipediaLists(
		echo=progress_bar,
		wikipedia_lists={
			**get_charity_guides(wikipedia=wikipedia, echo=progress_bar),
			**get_ngo_guides(wikipedia=wikipedia, echo=progress_bar),
			**get_temple_guides(wikipedia=wikipedia, echo=progress_bar),
			**get_political_party_guides(wikipedia=wikipedia, echo=progress_bar),
			**get_terrorist_group_guides(wikipedia=wikipedia, echo=progress_bar),
			**get_univesity_guides(wikipedia=wikipedia, echo=progress_bar),
			**get_sports_team_guides(wikipedia=wikipedia, echo=progress_bar),
			**get_intergovernmental(wikipedia=wikipedia, echo=progress_bar)

		}
	)
