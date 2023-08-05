from chronometry.progress import ProgressBar
from ..WikipediaListGuide import WikipediaListGuide
from ..WikipediaLists import WikipediaLists

COMPANY = 'company'


def get_company_list_guides(wikipedia=None, echo=0):
	"""
	:param wikipedia:
	:param echo: int or ProgressBar or bool
	:rtype: dict[str, WikipediaListGuide]
	"""
	return {
		'record_label': WikipediaListGuide(
			list_type='list_of_lists', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'record_label'],
			urls='https://en.wikipedia.org/wiki/List_of_record_labels'
		),
		'lists_of_airlines': WikipediaListGuide(
			list_type='list_of_lists', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'airline'],
			columns={COMPANY: 'airline'},
			urls=[
				'https://en.wikipedia.org/wiki/Lists_of_airlines'
			]
		),
		'public_company': WikipediaListGuide(
			list_type='list_of_lists', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'public_company'],
			urls=[
				'https://en.wikipedia.org/wiki/Lists_of_companies_by_stock_exchange_listing',
				'https://en.wikipedia.org/wiki/FTSE_100_Index',
				'https://en.wikipedia.org/wiki/FTSE_250_Index'
			],
			columns={COMPANY: ['issuer_name', COMPANY, 'english_name', 'stock_name', 'short_name', 'full_name']}
		),
		'american_newspapers_lists': WikipediaListGuide(
			list_type='list_of_lists', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia,
			categories=[COMPANY, 'newspaper', 'american'],
			urls='https://en.wikipedia.org/wiki/List_of_newspapers_in_the_United_States',
			sections=['By state and territory'],
			columns={COMPANY: ['newspaper', 'name', 'title']},
			exclude_urls=[
				'https://en.wikipedia.org/wiki/List_of_newspapers_in_Michigan',
				'https://en.wikipedia.org/wiki/List_of_newspapers_in_Rhode_Island'
			]
		),
		'automotive_fuel_retail': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'automotive_fuel_retail'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_automotive_fuel_retailers'
		),
		'sports_car_manufacturers': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'car_manufacturer', 'sports_car_manufacturer'],
			representation='table',
			columns={COMPANY: 'manufacturer'},
			urls='https://en.wikipedia.org/wiki/List_of_automotive_fuel_retailers'
		),
		'bicycle': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'bicycle'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_bicycle_brands_and_manufacturing_companies'
		),
		'bicycle_part': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'bicycle_part'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_bicycle_part_manufacturing_companies'
		),
		'car_audio': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'car_audio'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_car_audio_manufacturers_and_brands'
		),
		'defunct': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'defunct'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_defunct_consumer_brands'
		),
		'digital_camera': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'digital_camera'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_digital_camera_brands'
		),
		'electronics': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'electronics'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_electronics_brands',
			sections=['Asia', 'Europe', 'North America', 'Oceania', 'South America']),
		'italian': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'italian'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_Italian_brands'
		),
		'mexican': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'mexican'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_Mexican_brands'
		),
		'microbrewery': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'microbrewery'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_microbreweries'
		),
		'mountaineering_equipment': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'mountaineering_equipment'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_mountaineering_equipment_brands'
		),
		'piano': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'piano'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_piano_brand_names'
		),
		'motorcycle': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'motorcycle'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_motorcycle_manufacturers'
		),
		'sewing_machine': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'sewing_machine'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_sewing_machine_brands'
		),
		'video_telecommunication': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'video_telecommunication'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_video_telecommunication_services_and_product_brands'
		),
		'soft_drink': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'soft_drink'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_soft_drink_producers'
		),
		'frozen_food': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'frozen_food'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_frozen_food_brands'
		),
		'bakery': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'bakery'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_bakeries'
		),
		'cleaning': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'cleaning'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_cleaning_companies'
		),
		'named_after_people': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'named_after_people'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_companies_named_after_people'
		),
		'conglomerates': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'conglomerates'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_conglomerates'
		),
		'sony_subsidiary': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'sony_subsidiary'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_Sony_subsidiaries'
		),
		'canadian_national_railway': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'canadian_national_railway'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_Canadian_National_Railways_companies'
		),
		'canadian_pacific_railway_subsidiary': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'canadian_pacific_railway_subsidiary'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_subsidiary_railways_of_the_Canadian_Pacific_Railway'
		),
		'drive_in_theater': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'drive_in_theater'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_drive-in_theaters'
		),
		'elevator': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'elevator'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_elevator_manufacturers'
		),
		'employee_owned': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'employee_owned'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_employee-owned_companies'
		),
		'private_equity': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'private_equity'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_private_equity_firms'
		),
		'etymology': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'etymology'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_company_name_etymologies'
		),
		'franchises': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'franchises'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_franchises'
		),
		'holding': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'holding'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_holding_companies'
		),
		'reestablished': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'reestablished'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_re-established_companies'
		),
		'switched_industry': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'switched_industry'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_companies_that_switched_industries'
		),
		'government_owned': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'government_owned'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_government-owned_companies'
		),
		'multinational': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'multinational'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_multinational_corporations'
		),
		'past_ftse_100': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'past_ftse_100'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/FTSE_100_Index', sections='Past constituents'
		),
		'advertising': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'advertising'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_advertising_technology_companies'
		),
		'animation_distribution': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'animation_distribution'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_animation_distribution_companies'
		),
		'anime': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'anime'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_anime_companies'
		),
		'asset_management': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'asset_management'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_asset_management_firms'
		),
		'latin_american_broadcasting': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'latin_american_broadcasting'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_broadcasting_companies_in_Latin_America'
		),
		'cable_tv': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'cable_tv'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_cable_television_companies'
		),
		'casino': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'casino'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_casinos'
		),
		'clock': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'clock'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_clock_manufacturers'
		),
		'computer_hardware': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'computer_hardware'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_computer_hardware_manufacturers'
		),
		'computer_system': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'computer_system'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_computer_system_manufacturers'
		),
		'concentrating_solar_thermal_power': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'concentrating_solar_thermal_power'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_concentrating_solar_thermal_power_companies'
		),
		'book_distributor': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'book_distributor'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_book_distributors'
		),
		'film_distributor': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'film_distributor'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_film_distributors_by_country'
		),
		'duty_free': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'duty_free'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_duty-free_shops'
		),
		'frozen_custard': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'frozen_custard'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_frozen_custard_companies'
		),
		'enterprise_search_vendor': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'enterprise_search_vendor'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_enterprise_search_vendors',
			sections='Vendors of prop'
		),
		'north_american_filling_station': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'north_american', 'filling_station'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_filling_station_chains_in_North_America'
		),
		'food': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'food'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_food_companies'
		),
		'defunct_gambling': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'defunct_gambling'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_defunct_gambling_companies'
		),
		'home_video': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'home_video'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_home_video_companies'
		),
		'food_truck': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'food_truck'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_food_trucks'
		),
		'ice': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'ice'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_ice_companies'
		),
		'seafood': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'seafood'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_seafood_companies'
		),
		'teahouse': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'teahouse'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_teahouses'
		),
		'trading': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'trading'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_trading_companies'
		),
		'management_consulting': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'management_consulting'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_management_consulting_firms'
		),
		'marketing_research': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'marketing_research'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_marketing_research_firms'
		),
		'modeling_agency': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'modeling_agency'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_modeling_agencies'
		),
		'multilevel_marketing': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'multilevel_marketing'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_multi-level_marketing_companies'
		),
		'american_mutual_fund': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'american', 'mutual_fund'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_mutual-fund_families_in_the_United_States'
		),
		'open_game_license_publisher': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'open_game_license_publisher'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_OGL_publishers'
		),
		'petroleum': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'petroleum'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_oil_exploration_and_production_companies'
		),
		'oilfield_service': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'oilfield_service'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_oilfield_service_companies'
		),
		'pharmaceutical': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'pharmaceutical'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_pharmaceutical_companies'
		),
		'pornographic_studio': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'pornographic_studio'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_pornographic_film_studios'
		),
		'defunct_fast_food': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'defunct_fast_food'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_defunct_fast-food_restaurant_chains'
		),
		'private_security': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'private_security'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_private_security_companies'
		),
		'freight_ship': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'freight_ship'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_freight_ship_companies'
		),
		'passenger_ship': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'passenger_ship'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_passenger_ship_companies'
		),
		'silicon': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'silicon'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_silicon_producers'
		),
		'steel': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'steel'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_steel_producers'
		),
		'system_on_a_chip': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'system_on_a_chip'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_system-on-a-chip_suppliers'
		),
		'tea': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'tea'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_tea_companies'
		),
		'television_network': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'television_network'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_television_networks_by_country'
		),
		'winery': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'winery'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_vineyards_and_wineries'
		),
		'aircraft': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'aircraft'],
			representation='list',
			urls=[
				'https://en.wikipedia.org/wiki/List_of_aircraft_manufacturers:_A',
				'https://en.wikipedia.org/wiki/List_of_aircraft_manufacturers:_B-C',
				'https://en.wikipedia.org/wiki/List_of_aircraft_manufacturers:_D-G',
				'https://en.wikipedia.org/wiki/List_of_aircraft_manufacturers_H-L',
				'https://en.wikipedia.org/wiki/List_of_aircraft_manufacturers:_M-P',
				'https://en.wikipedia.org/wiki/List_of_aircraft_manufacturers:_Q-S',
				'https://en.wikipedia.org/wiki/List_of_aircraft_manufacturers:_T-Z',
			]
		),
		'rotorcraft': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'rotorcraft'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_rotorcraft_manufacturers_by_country'
		),
		'helicopter_airline': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'helicopter_airline'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_helicopter_airlines'
		),
		'bank': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'bank'],
			columns={COMPANY: ['bank_name']},
			urls=[
				'https://en.wikipedia.org/wiki/List_of_banks_(alphabetical)',
				'https://en.wikipedia.org/wiki/List_of_banks_in_India'
			]
		),
		'investment_bank': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'investment_bank'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_investment_banks'
		),
		'bookstore': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'bookstore'],
			representation='list',
			urls=[
				'https://en.wikipedia.org/wiki/List_of_independent_bookstores_in_the_United_States',
				'https://en.wikipedia.org/wiki/List_of_independent_bookstores'
			]
		),
		'bookstore_chain': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'bookstore_chain'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_bookstore_chains'
		),
		'ice_cream_parlor': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'ice_cream_parlor'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_ice_cream_parlor_chains'
		),
		'resaurant_chain': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'resaurant_chain'],
			representation='list',
			urls=[
				'https://en.wikipedia.org/wiki/List_of_restaurant_chains',
				'https://en.wikipedia.org/wiki/List_of_fast_food_restaurant_chains',
				'https://en.wikipedia.org/wiki/List_of_pizza_chains',
				'https://en.wikipedia.org/wiki/List_of_pizza_franchises'
			]
		),
		'law_firm': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=['law_firm', 'european'],
			representation='list',
			urls='https://en.wikipedia.org/wiki/List_of_largest_Europe-based_law_firms_by_revenue'
		),
		'tv_channel': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'tv_channel'],
			representation='list',
			urls=[
				'https://en.wikipedia.org/wiki/List_of_movie_television_channels',
				'https://en.wikipedia.org/wiki/List_of_generalist_television_channels',
				'https://en.wikipedia.org/wiki/List_of_music_video_television_channels'
			]
		),
		'hotel': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'hotel'],
			representation='table', columns={COMPANY: COMPANY},
			urls='https://en.wikipedia.org/wiki/List_of_chained-brand_hotels'
		),
		'laptop': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'laptop'],
			representation='table', columns={COMPANY: ['name', 'brand']},
			urls='https://en.wikipedia.org/wiki/List_of_laptop_brands_and_manufacturers',
			sections=['Brands', 'Other brands']),
		'ski': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'ski'],
			representation='table', columns={COMPANY: 'name_of_brand'},
			urls='https://en.wikipedia.org/wiki/List_of_ski_brands'
		),
		'swimwear': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'swimwear'],
			representation='table', columns={COMPANY: 'brand'},
			urls='https://en.wikipedia.org/wiki/List_of_swimwear_brands'
		),

		'copper': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'copper'],
			representation='table', columns={COMPANY: COMPANY},
			urls='https://en.wikipedia.org/wiki/List_of_copper_production_by_company'
		),
		'fortune_global_500': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'fortune_global_500'],
			representation='table', columns={COMPANY: COMPANY},
			urls='https://en.wikipedia.org/wiki/Fortune_Global_500'
		),
		'financial_services': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'financial_services'],
			representation='table', columns={COMPANY: COMPANY},
			urls='https://en.wikipedia.org/wiki/List_of_largest_financial_services_companies_by_revenue'
		),
		'largest_internet': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'internet'],
			representation='table', columns={COMPANY: COMPANY},
			urls='https://en.wikipedia.org/wiki/List_of_largest_Internet_companies',
			sections='List'
		),
		'largest_technology': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'technology'],
			representation='table', columns={COMPANY: 'company_2'},
			urls='https://en.wikipedia.org/wiki/List_of_largest_technology_companies_by_revenue',
			sections='List'
		),
		'largest_software': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'software'],
			representation='table', columns={COMPANY: 'organization_2'},
			urls='https://en.wikipedia.org/wiki/List_of_the_largest_software_companies',
			sections='Forbes Global 2000'
		),
		'private_equity_table': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'private_equity'],
			representation='table', columns={COMPANY: ['private_equity_firm', 'firm']},
			urls='https://en.wikipedia.org/wiki/List_of_private_equity_firms'
		),
		'involved_in_holocaust': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'involved_in_holocaust'],
			representation='table', columns={COMPANY: 'company_name'},
			urls='https://en.wikipedia.org/wiki/List_of_companies_involved_in_the_Holocaust'
		),
		'oldest': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'old'],
			representation='table', columns={COMPANY: COMPANY},
			urls='https://en.wikipedia.org/wiki/List_of_oldest_companies'
		),
		's_and_p_400': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 's_and_p_400'],
			representation='table', columns={COMPANY: 'security'},
			urls='https://en.wikipedia.org/wiki/List_of_S%26P_400_companies'
		),
		's_and_p_500': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 's_and_p_500'],
			representation='table', columns={COMPANY: 'security'},
			urls='https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
		),
		'largest_by_revenue': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'high_revenue'],
			representation='table', columns={COMPANY: 'name'},
			urls='https://en.wikipedia.org/wiki/List_of_largest_companies_by_revenue'
		),
		'largest_european_manufacturing': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=['manufacturing', 'european'],
			representation='table', columns={COMPANY: COMPANY},
			urls='https://en.wikipedia.org/wiki/List_of_largest_European_manufacturing_companies_by_revenue'
		),
		'ftse_100': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'ftse_100'],
			representation='table', columns={COMPANY: COMPANY},
			urls='https://en.wikipedia.org/wiki/FTSE_100_Index'
		),
		'unicorn_startup': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=['startup', 'unicorn_startup'],
			representation='table', columns={COMPANY: COMPANY},
			urls='https://en.wikipedia.org/wiki/List_of_unicorn_startup_companies'
		),
		'animation_studio': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'animation_studio'],
			representation='table', columns={COMPANY: 'studio'},
			urls='https://en.wikipedia.org/wiki/List_of_animation_studios'
		),
		'largest_biotechnology': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'biotechnology'],
			representation='table', columns={COMPANY: COMPANY},
			urls='https://en.wikipedia.org/wiki/List_of_largest_biotechnology_and_pharmaceutical_companies'
		),
		'bullion_dealer': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'bullion_dealer'],
			representation='table', columns={COMPANY: 'dealer'},
			urls='https://en.wikipedia.org/wiki/List_of_bullion_dealers'
		),
		'computer_aided_technology': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'computer_aided_technology'],
			representation='table', columns={COMPANY: 'company_name'},
			urls='https://en.wikipedia.org/wiki/List_of_CAx_companies'
		),
		'champagne_house': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'champagne_house'],
			representation='table', columns={COMPANY: 'house'},
			urls='https://en.wikipedia.org/wiki/List_of_Champagne_houses'
		),
		'coffee': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'coffee'],
			representation='table', columns={COMPANY: 'company_name'},
			urls='https://en.wikipedia.org/wiki/List_of_coffee_companies'
		),
		'electronic_design_automation': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'electronic_design_automation'],
			representation='table', columns={COMPANY: COMPANY},
			urls='https://en.wikipedia.org/wiki/List_of_EDA_companies'
		),
		'film_production': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'film_production'],
			representation='table', columns={COMPANY: COMPANY},
			urls='https://en.wikipedia.org/wiki/List_of_live-action_film_production_companies'
		),
		'former_investment_bank': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=['former', 'investment_bank'],
			representation='table', columns={COMPANY: 'firm'},
			urls='https://en.wikipedia.org/wiki/List_of_investment_banks',
			sections=['Notable former investment banks and brokerages']
		),
		'largest_chemical_producer': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'chemical_producer'],
			representation='table', columns={COMPANY: COMPANY},
			urls='https://en.wikipedia.org/wiki/List_of_largest_chemical_producers'
		),
		'mobile_network': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'mobile_network'],
			representation='table', columns={COMPANY: [COMPANY, 'operator']},
			urls=[
				'https://en.wikipedia.org/wiki/List_of_mobile_network_operators',
				'https://en.wikipedia.org/wiki/List_of_mobile_network_operators_of_Europe',
				'https://en.wikipedia.org/wiki/List_of_mobile_network_operators_of_the_Americas',
				'https://en.wikipedia.org/wiki/List_of_mobile_network_operators_of_the_Asia_Pacific_region',
				'https://en.wikipedia.org/wiki/List_of_mobile_network_operators_of_the_Middle_East_and_Africa',
				'https://en.wikipedia.org/wiki/List_of_Canadian_mobile_phone_companies',
				'https://en.wikipedia.org/wiki/List_of_mobile_network_operators_of_The_Caribbean',
				'https://en.wikipedia.org/wiki/List_of_United_States_wireless_communications_service_providers'
			]
		),

		'canadian_mutual_fund': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=['canadian', 'mutual_fund'],
			representation='table', columns={COMPANY: 'ultimate_parent'},
			urls='https://en.wikipedia.org/wiki/List_of_mutual-fund_families_in_Canada'
		),
		'largest_oil_and_gas': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'oil_and_gas'],
			representation='table', columns={COMPANY: 'company_name'},
			urls='https://en.wikipedia.org/wiki/List_of_largest_oil_and_gas_companies_by_revenue'
		),
		'photo_voltaic': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'photo_voltaic'],
			representation='table', columns={COMPANY: COMPANY},
			urls='https://en.wikipedia.org/wiki/List_of_photovoltaics_companies'
		),
		'pornography': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'pornography'],
			representation='table', columns={COMPANY: 'name'},
			urls='https://en.wikipedia.org/wiki/List_of_pornography_companies'
		),
		'european_power': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=['european', 'power'],
			representation='table', columns={COMPANY: COMPANY},
			urls='https://en.wikipedia.org/wiki/List_of_European_power_companies_by_carbon_intensity',
		),
		'container_shipping': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'container_shipping'],
			representation='table', columns={COMPANY: COMPANY},
			urls='https://en.wikipedia.org/wiki/List_of_largest_container_shipping_companies'
		),
		'private_spaceflight': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=['spaceflight', 'private'],
			representation='table', columns={COMPANY: 'company_name'},
			urls='https://en.wikipedia.org/wiki/List_of_private_spaceflight_companies'
		),
		'steel_table': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'steel'],
			representation='table', columns={COMPANY: COMPANY},
			urls='https://en.wikipedia.org/wiki/List_of_steel_producers'
		),
		'telephone': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'telephone'],
			representation='table', columns={COMPANY: COMPANY},
			urls='https://en.wikipedia.org/wiki/List_of_telephone_operating_companies'
		),
		'venture_capital': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'venture_capital'],
			representation='table', columns={COMPANY: 'name'},
			urls='https://en.wikipedia.org/wiki/List_of_venture_capital_firms'
		),
		'video_game_developer': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=['video_game', 'video_game_developer'],
			representation='table', columns={COMPANY: 'developer'},
			urls=[
				'https://en.wikipedia.org/wiki/List_of_video_game_developers',
				'https://en.wikipedia.org/wiki/List_of_PlayStation_3_games_released_on_disc'
			]
		),
		'video_game_publisher': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=['video_game', 'video_game_publisher'],
			representation='table', columns={COMPANY: 'publisher'},
			urls=[
				'https://en.wikipedia.org/wiki/List_of_video_game_publishers',
				'https://en.wikipedia.org/wiki/List_of_video_games_considered_the_best'
			]
		),
		'indie_game_developer': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=['video_game', 'indie_game_developer'],
			representation='table', columns={COMPANY: 'developer'},
			urls='https://en.wikipedia.org/wiki/List_of_indie_game_developers'
		),
		'flag_carrier': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'flag_carrier'],
			representation='table', columns={COMPANY: 'airline'},
			urls='https://en.wikipedia.org/wiki/Flag_carrier'
		),
		'airline': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'airline'],
			columns={COMPANY: 'airline'},
			urls=[
				'https://en.wikipedia.org/wiki/List_of_airlines_with_more_than_100_destinations',
				'https://en.wikipedia.org/wiki/World%27s_largest_airlines',
				'https://en.wikipedia.org/wiki/List_of_low-cost_airlines',
				'https://en.wikipedia.org/wiki/List_of_regional_airlines',
				'https://en.wikipedia.org/wiki/List_of_airlines_of_Australia'
			]
		),
		'coffeehouse': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'coffeehouse'],
			representation='table', columns={COMPANY: 'name'},
			urls='https://en.wikipedia.org/wiki/List_of_coffeehouse_chains'
		),
		'restaurant_chain': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'restaurant_chain'],
			representation='table', columns={COMPANY: 'name'},
			urls=[
				'https://en.wikipedia.org/wiki/List_of_restaurant_chains',
				'https://en.wikipedia.org/wiki/List_of_casual_dining_restaurant_chains'
			]
		),
		'law_firm_table': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'law_firm'],
			representation='table', columns={COMPANY: ['firm', 'name', 'firm_name']},
			urls=[
				'https://en.wikipedia.org/wiki/List_of_largest_law_firms_by_revenue',
				'https://en.wikipedia.org/wiki/List_of_largest_Canada-based_law_firms_by_revenue',
				'https://en.wikipedia.org/wiki/List_of_largest_United_States-based_law_firms_by_head_count',
				'https://en.wikipedia.org/wiki/List_of_largest_Japan-based_law_firms_by_head_count',
				'https://en.wikipedia.org/wiki/List_of_US_law_firms_by_profits_per_partner'
			]
		),

		'tv_channel_table': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'tv_channel'],
			representation='table', columns={COMPANY: ['name', 'network']},
			urls=[
				'https://en.wikipedia.org/wiki/List_of_documentary_television_channels',
				'https://en.wikipedia.org/wiki/List_of_news_television_channels',
			]
		),
		'forbes_global_2000': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'forbes_global_2000'],
			representation='table', columns={COMPANY: COMPANY},
			urls='https://en.wikipedia.org/wiki/Forbes_Global_2000'
		),
		'largest_nordic': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'nordic'],
			representation='table', columns={COMPANY: COMPANY},
			urls='https://en.wikipedia.org/wiki/List_of_largest_Nordic_companies'
		),
		'mobile_phone_maker': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'mobile_phone_maker'],
			representation='table', columns={COMPANY: 'brand'},
			urls='https://en.wikipedia.org/wiki/List_of_mobile_phone_brands_by_country'),
		'stock_exchange': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia, categories=[COMPANY, 'stock_exchange'],
			columns={COMPANY: ['stock_exchange', 'exchange']},
			urls=[
				'https://en.wikipedia.org/wiki/List_of_stock_exchanges',
				'https://en.wikipedia.org/wiki/List_of_stock_exchanges_in_the_Americas',
				'https://en.wikipedia.org/wiki/List_of_Asian_stock_exchanges',
				'https://en.wikipedia.org/wiki/List_of_European_stock_exchanges',
				'https://en.wikipedia.org/wiki/List_of_African_stock_exchanges',
				'https://en.wikipedia.org/wiki/List_of_stock_exchanges_in_Oceania'
			]
		),
		'newspapers': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia,
			categories=[COMPANY, 'newspaper', 'british_newspaper', 'british'],
			urls=[
				'https://en.wikipedia.org/wiki/List_of_newspapers_in_the_United_Kingdom'
			],
			columns={COMPANY: ['title']}
		),
		'american_newspapers': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia,
			categories=[COMPANY, 'newspaper', 'american'],
			urls='https://en.wikipedia.org/wiki/List_of_newspapers_in_the_United_States',
			sections=['Top 10 newspapers by circulation', 'Longest running newspaper'],
			columns={COMPANY: ['newspaper']}
		),
		'american_companies': WikipediaListGuide(
			list_type='list', data_type=COMPANY, echo=echo - 1,
			wikipedia=wikipedia,
			categories=[COMPANY, 'american'],
			urls=[
				'https://en.wikipedia.org/wiki/List_of_companies_of_the_United_States_by_state',
				'https://en.wikipedia.org/wiki/List_of_Alabama_companies',
				'https://en.wikipedia.org/wiki/List_of_Alaska_companies',
				'https://en.wikipedia.org/wiki/List_of_Arizona_companies',
				'https://en.wikipedia.org/wiki/List_of_Arkansas_companies',
				'https://en.wikipedia.org/wiki/List_of_California_companies',
				'https://en.wikipedia.org/wiki/List_of_Colorado_companies',
				'https://en.wikipedia.org/wiki/List_of_Connecticut_companies',
				'https://en.wikipedia.org/wiki/List_of_Delaware_companies',
				'https://en.wikipedia.org/wiki/List_of_Florida_companies',
				'https://en.wikipedia.org/wiki/List_of_Georgia_(U.S._state)_companies',
				'https://en.wikipedia.org/wiki/List_of_companies_based_in_Idaho',
				'https://en.wikipedia.org/wiki/List_of_Illinois_companies',
				'https://en.wikipedia.org/wiki/List_of_Kansas_companies',
				'https://en.wikipedia.org/wiki/List_of_Kentucky_companies',
				'https://en.wikipedia.org/wiki/List_of_Massachusetts_companies',
				'https://en.wikipedia.org/wiki/List_of_Michigan_companies',
				'https://en.wikipedia.org/wiki/List_of_Minnesota_companies',
				'https://en.wikipedia.org/wiki/List_of_North_Dakota_companies',
				'https://en.wikipedia.org/wiki/List_of_companies_in_Greater_Cincinnati',
				'https://en.wikipedia.org/wiki/List_of_companies_based_in_Oklahoma_City',
				'https://en.wikipedia.org/wiki/List_of_companies_based_in_Tulsa,_Oklahoma',
				'https://en.wikipedia.org/wiki/List_of_companies_based_in_Oregon',
				'https://en.wikipedia.org/wiki/List_of_companies_based_in_the_Harrisburg_area',
				'https://en.wikipedia.org/wiki/List_of_companies_based_in_the_Philadelphia_area',
				'https://en.wikipedia.org/wiki/List_of_corporations_in_Pittsburgh',
				'https://en.wikipedia.org/wiki/List_of_Rhode_Island_companies',
				'https://en.wikipedia.org/wiki/List_of_companies_based_in_Nashville,_Tennessee',
				'https://en.wikipedia.org/wiki/List_of_Texas_companies',
				'https://en.wikipedia.org/wiki/List_of_Utah_companies',
				'https://en.wikipedia.org/wiki/List_of_companies_headquartered_in_Northern_Virginia',
				'https://en.wikipedia.org/wiki/List_of_Washington_(state)_companies',
				'https://en.wikipedia.org/wiki/List_of_Wyoming_companies',
				'https://en.wikipedia.org/wiki/List_of_restaurants_in_Hawaii',
				'https://en.wikipedia.org/wiki/List_of_airlines_of_Hawaii'
			],
			columns={COMPANY: ['name', 'corporation']}
		)
	}

def get_companies(wikipedia=None, echo=0):
	echo = max(0, echo)
	progress_bar = ProgressBar(echo=echo, total=None)
	list_guides = get_company_list_guides(wikipedia=wikipedia, echo=progress_bar)
	return WikipediaLists(wikipedia_lists=list_guides, categories=[COMPANY], echo=progress_bar)
