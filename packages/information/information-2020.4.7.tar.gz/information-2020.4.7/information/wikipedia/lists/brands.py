from ..WikipediaListGuide import WikipediaListGuide
from ..WikipediaLists import WikipediaLists
from chronometry.progress import ProgressBar

BRAND = 'brand'
BRAND_OR_COMPANY = 'brand_or_company'

def get_brand_list_guides(wikipedia=None, echo=0):
	brand_lists = {
		'car_brands': WikipediaListGuide(
			list_type='list', data_type=BRAND, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND, 'car_brand'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_car_brands'
		),
		'car_brands_2': WikipediaListGuide(
			list_type='list', data_type=BRAND, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND, 'car_brand'],
			representation='table',
			sections=['Brand bestsellers'],
			columns={BRAND: ['brand']},
			urls='https://en.wikipedia.org/wiki/List_of_best-selling_automobiles'
		),
		'procter_and_gamble': WikipediaListGuide(
			list_type='list', data_type=BRAND, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND, 'procter_and_gamble'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_Procter_%26_Gamble_brands'
		),
		'unilever': WikipediaListGuide(
			list_type='list', data_type=BRAND, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND, 'unilever'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_Unilever_brands'
		),
		'cocacola': WikipediaListGuide(
			list_type='list', data_type=BRAND, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND, 'cocacola'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_Coca-Cola_brands'
		),
		'keurig': WikipediaListGuide(
			list_type='list', data_type=BRAND, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND, 'keurig'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_Keurig_Dr_Pepper_brands'
		),
		'molson': WikipediaListGuide(
			list_type='list', data_type=BRAND, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND, 'molson'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_Molson_Coors_brands'
		),
		'pepsi': WikipediaListGuide(
			list_type='list', data_type=BRAND, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND, 'pepsi'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_Pepsi_variations'
		),
		'conagra': WikipediaListGuide(
			list_type='list', data_type=BRAND, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND, 'conagra'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_Conagra_brands'
		),
		'kraft': WikipediaListGuide(
			list_type='list', data_type=BRAND, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND, 'kraft'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_Kraft_brands'
		),
		'nestle': WikipediaListGuide(
			list_type='list', data_type=BRAND, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND, 'nestle'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_Nestl%C3%A9_brands'
		),
		'british_rail': WikipediaListGuide(
			list_type='list', data_type=BRAND, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND, 'british_rail'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/British_Rail_brand_names'
		),
		'toy': WikipediaListGuide(
			list_type='list', data_type=BRAND, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND, 'toy'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_toys'
		),
		'toothpaste': WikipediaListGuide(
			list_type='list', data_type=BRAND, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND, 'toothpaste'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_toothpaste_brands'
		),
		'rolling_paper': WikipediaListGuide(
			list_type='list', data_type=BRAND, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND, 'rolling_paper'],
			representation='table', columns={BRAND: 'name'},
			urls='https://en.wikipedia.org/wiki/List_of_rolling_papers'
		),
		'fitness_wear': WikipediaListGuide(
			list_type='list', data_type=BRAND, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND, 'fitness_wear'],
			representation='list', 
			urls='https://en.wikipedia.org/wiki/List_of_fitness_wear_brands'
		),
		'japanese_bicycle': WikipediaListGuide(
			list_type='list', data_type=BRAND, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND, 'japanese_bicycle'],
			representation='list', 
			urls='https://en.wikipedia.org/wiki/List_of_Japanese_bicycle_brands_and_manufacturers'
		),
		'molson_coors': WikipediaListGuide(
			list_type='list', data_type=BRAND, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND, 'molson_coors'],
			representation='list', 
			urls='https://en.wikipedia.org/wiki/List_of_Molson_Coors_brands'
		),
		'rum': WikipediaListGuide(
			list_type='list', data_type=BRAND, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND, 'rum'],
			representation='list', 
			urls='https://en.wikipedia.org/wiki/List_of_rum_producers'
		),
		'soft_drink': WikipediaListGuide(
			list_type='list', data_type=BRAND, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND, 'soft_drink'],
			representation='list', 
			urls='https://en.wikipedia.org/wiki/List_of_soft_drinks_by_country'
		),
		'tequila': WikipediaListGuide(
			list_type='list', data_type=BRAND, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND, 'tequila'],
			representation='list', 
			urls='https://en.wikipedia.org/wiki/List_of_tequilas'
		),
		'whisky': WikipediaListGuide(
			list_type='list', data_type=BRAND, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND, 'whisky'],
			representation='list', 
			urls='https://en.wikipedia.org/wiki/List_of_whisky_brands'
		),
		'bread': WikipediaListGuide(
			list_type='list', data_type=BRAND, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND, 'bread'],
			representation='list', 
			urls='https://en.wikipedia.org/wiki/List_of_brand_name_breads'
		),
		'confectionery': WikipediaListGuide(
			list_type='list', data_type=BRAND, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND, 'confectionery'],
			representation='list', 
			urls='https://en.wikipedia.org/wiki/List_of_confectionery_brands'
		),
		'food': WikipediaListGuide(
			list_type='list', data_type=BRAND, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND, 'food'],
			representation='list', 
			urls='https://en.wikipedia.org/wiki/List_of_brand_name_food_products'
		),
		'frozen_dessert': WikipediaListGuide(
			list_type='list', data_type=BRAND, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND, 'frozen_dessert'],
			representation='list', 
			urls='https://en.wikipedia.org/wiki/List_of_frozen_dessert_brands'
		),
		'mustard': WikipediaListGuide(
			list_type='list', data_type=BRAND, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND, 'mustard'],
			representation='list', 
			urls='https://en.wikipedia.org/wiki/List_of_mustard_brands'
		),
		'lingerie': WikipediaListGuide(
			list_type='list', data_type=BRAND_OR_COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND, 'lingerie'],
			representation='table', columns={BRAND_OR_COMPANY: 'brand'},
			urls='https://en.wikipedia.org/wiki/List_of_lingerie_brands'
		),
		'cider': WikipediaListGuide(
			list_type='list', data_type=BRAND_OR_COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND, 'cider'],
			representation='table', columns={BRAND_OR_COMPANY: 'name'},
			urls='https://en.wikipedia.org/wiki/List_of_cider_brands'
		),
		'candy': WikipediaListGuide(
			list_type='list', data_type=BRAND_OR_COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND, 'candy'],
			representation='table', columns={BRAND_OR_COMPANY: 'top_brands'},
			urls='https://en.wikipedia.org/wiki/List_of_top-selling_candy_brands'
		),
		'popcorn': WikipediaListGuide(
			list_type='list', data_type=BRAND_OR_COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND, 'popcorn'],
			representation='table', columns={BRAND_OR_COMPANY: 'name'},
			urls='https://en.wikipedia.org/wiki/List_of_popcorn_brands'
		),
		'firearm': WikipediaListGuide(
			list_type='list', data_type=BRAND_OR_COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND_OR_COMPANY, 'firearm'],
			representation='table', columns={'company': 'company', 'brand': 'marque'},
			urls='https://en.wikipedia.org/wiki/List_of_firearm_brands'
		),
		'perfume': WikipediaListGuide(
			list_type='list', data_type=BRAND_OR_COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND_OR_COMPANY, 'perfume'],
			representation='table', columns={'company': 'company', 'brand': 'name'},
			urls='https://en.wikipedia.org/wiki/List_of_perfumes'
		),
		'vodka': WikipediaListGuide(
			list_type='list', data_type=BRAND, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND_OR_COMPANY, 'vodka'],
			representation='table', columns={BRAND: 'brand'},
			urls='https://en.wikipedia.org/wiki/List_of_vodkas'
		),
		'breath_mint': WikipediaListGuide(
			list_type='list', data_type=BRAND, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND_OR_COMPANY, 'breath_mint'],
			representation='table', columns={BRAND: 'name', 'company': 'company'},
			urls='https://en.wikipedia.org/wiki/List_of_breath_mints'
		),
		'chewing_gum': WikipediaListGuide(
			list_type='list', data_type=BRAND, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND_OR_COMPANY, 'chewing_gum'],
			representation='table', columns={BRAND: 'name', 'company': 'parent_company'},
			urls='https://en.wikipedia.org/wiki/List_of_chewing_gum_brands'
		),
		'chocolate_bar': WikipediaListGuide(
			list_type='list', data_type=BRAND, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND_OR_COMPANY, 'chocolate_bar'],
			representation='table', columns={BRAND: 'name', 'company': 'manufacturer'},
			urls='https://en.wikipedia.org/wiki/List_of_chocolate_bar_brands'
		),
		'instant_noodle': WikipediaListGuide(
			list_type='list', data_type=BRAND, echo=echo - 1,
			wikipedia=wikipedia, categories=[BRAND_OR_COMPANY, 'instant_noodle'],
			representation='table', columns={BRAND: 'name', 'company': 'current_owner'},
			urls='https://en.wikipedia.org/wiki/List_of_instant_noodle_brands'
		)
	}
	return brand_lists


def get_brands(wikipedia=None, echo=0):
	echo = max(0, echo)
	progress_bar = ProgressBar(echo=echo, total=None)
	list_guides = get_brand_list_guides(wikipedia=wikipedia, echo=progress_bar)
	return WikipediaLists(wikipedia_lists=list_guides, categories=[BRAND], echo=progress_bar)
