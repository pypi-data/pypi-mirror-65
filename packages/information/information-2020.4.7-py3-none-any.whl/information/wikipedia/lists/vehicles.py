from ..WikipediaListGuide import WikipediaListGuide
from ..WikipediaLists import WikipediaLists
from chronometry.progress import ProgressBar

VEHICLE = 'vehicle'


def get_vehicles(wikipedia=None, echo=0):
	echo = max(0, echo)
	progress_bar = ProgressBar(echo=echo, total=None)

	aircrafts = {
		'civil_aircrafts': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=progress_bar - 1, data_type=VEHICLE,
			categories=[VEHICLE, 'aircraft', 'civil_aircraft'],
			urls='https://en.wikipedia.org/wiki/List_of_civil_aircraft',
			representation='list'
		),
		'bush_planes': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=progress_bar - 1, data_type=VEHICLE,
			categories=[VEHICLE, 'aircraft', 'bush_plane'],
			urls='https://en.wikipedia.org/wiki/Bush_plane',
			representation='list',
			sections=['Current and historical bush planes']
		),
		'light_transport_aircrafts': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=progress_bar - 1, data_type=VEHICLE,
			categories=[VEHICLE, 'aircraft', 'transport_aircraft', 'light_transport_aircraft'],
			urls='https://en.wikipedia.org/wiki/List_of_light_transport_aircraft',
			representation='table',
			columns={VEHICLE: ['model']}
		),
		'racing_aircrafts': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=progress_bar - 1, data_type=VEHICLE,
			categories=[VEHICLE, 'aircraft'],
			urls=[
				'https://en.wikipedia.org/wiki/List_of_racing_aircraft',
				'https://en.wikipedia.org/wiki/List_of_STOL_aircraft',
				'https://en.wikipedia.org/wiki/List_of_VTOL_aircraft',
				'https://en.wikipedia.org/wiki/List_of_seaplanes_and_amphibious_aircraft'
			],
			representation=None,
			columns={VEHICLE: ['type']}
		),
		'fighter_aircrafts': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=progress_bar - 1, data_type=VEHICLE,
			categories=[VEHICLE, 'aircraft', 'military_vehicle', 'military_aircraft', 'fighter_aircraft'],
			urls='https://en.wikipedia.org/wiki/List_of_fighter_aircraft',
			representation=None,
			columns={VEHICLE: ['type']}
		),
		'bomber_aircrafts': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=progress_bar - 1, data_type=VEHICLE,
			categories=[VEHICLE, 'aircraft', 'military_vehicle', 'military_aircraft', 'bomber_aircraft'],
			urls='https://en.wikipedia.org/wiki/List_of_bomber_aircraft',
			representation='table',
			columns={VEHICLE: ['type']}
		),
		'us_military_aircrafts': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=progress_bar - 1, data_type=VEHICLE,
			categories=[VEHICLE, 'aircraft', 'military_vehicle', 'military_aircraft', 'united_states_aircraft'],
			urls='https://en.wikipedia.org/wiki/List_of_active_United_States_military_aircraft',
			representation=None,
			columns={VEHICLE: ['type']}
		),
		'military_aircrafts': WikipediaListGuide(
			list_type='list_of_lists',
			wikipedia=wikipedia, echo=progress_bar - 1, data_type=VEHICLE,
			categories=[VEHICLE, 'aircraft', 'military_vehicle', 'military_aircraft'],
			urls='https://en.wikipedia.org/wiki/Category:Lists_of_military_aircraft',
			representation=None,
			columns={VEHICLE: ['type', 'aircraft']},
			sections=['Pages in category']
		)
	}

	ships = {
		'ships': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=progress_bar - 1, data_type=VEHICLE,
			categories=[VEHICLE, 'ship'],
			urls=[
				'https://en.wikipedia.org/wiki/List_of_cargo_ships',
				'https://en.wikipedia.org/wiki/Nuclear_marine_propulsion#Civilian_nuclear_ships',
				'https://en.wikipedia.org/wiki/List_of_cruise_ships',
				'https://en.wikipedia.org/wiki/List_of_river_cruise_ships',
				'https://en.wikipedia.org/wiki/List_of_largest_ferries_of_Europe',
				'https://en.wikipedia.org/wiki/List_of_icebreakers'
			],
			representation=None,
			columns={VEHICLE: ['name', 'ship']}
		),
		'liberty_ships': WikipediaListGuide(
			list_type='list_of_lists',
			wikipedia=wikipedia, echo=progress_bar - 1, data_type=VEHICLE,
			categories=[VEHICLE, 'ship', 'liberty_ship'],
			urls='https://en.wikipedia.org/wiki/List_of_Liberty_ships',
			representation='table', columns={VEHICLE: 'ship_name'}
		),
		'us_navy_ships': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=progress_bar - 1, data_type=VEHICLE,
			categories=[VEHICLE, 'ship', 'military_ship', 'united_states_navy', 'united_states_navy_ship'],
			urls='https://en.wikipedia.org/wiki/List_of_current_ships_of_the_United_States_Navy',
			representation='table',
			columns={VEHICLE: ['ship_name']}
		),
		'royal_canadian_navy_ships': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=progress_bar - 1, data_type=VEHICLE,
			categories=[VEHICLE, 'ship', 'military_ship', 'royal_canadian_navy', 'royal_canadian_navy_ship'],
			urls='https://en.wikipedia.org/wiki/List_of_ships_of_the_Royal_Canadian_Navy',
			representation='list'
		),
		'battleships': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=progress_bar - 1, data_type=VEHICLE,
			categories=[VEHICLE, 'ship', 'military_ship', 'battleship'],
			urls='https://en.wikipedia.org/wiki/List_of_battleships',
			representation='table',
			columns={VEHICLE: ['name']}
		),
		'us_navy_ship_classes': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=progress_bar - 1, data_type=VEHICLE,
			categories=[VEHICLE, 'ship', 'ship_class'],
			urls=[
				'https://en.wikipedia.org/wiki/List_of_current_ships_of_the_United_States_Navy',
				'https://en.wikipedia.org/wiki/List_of_battleships',
				'https://en.wikipedia.org/wiki/List_of_ships_of_the_Egyptian_Navy'
			],
			representation='table',
			columns={VEHICLE: ['class']}
		),
		'us_navy_ship_types': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=progress_bar - 1, data_type=VEHICLE,
			categories=[VEHICLE, 'ship', 'ship_type'],
			urls='https://en.wikipedia.org/wiki/List_of_current_ships_of_the_United_States_Navy',
			representation='table',
			columns={VEHICLE: ['type']}
		),
		'ocean_liners': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=progress_bar - 1, data_type=VEHICLE,
			categories=[VEHICLE, 'ship', 'ocean_liner'],
			urls='https://en.wikipedia.org/wiki/List_of_ocean_liners',
			representation='table',
			columns={VEHICLE: ['ship_name']}
		),
		'aircraft_carriers': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=progress_bar - 1, data_type=VEHICLE,
			categories=[VEHICLE, 'ship', 'military_ship', 'aircraft_carrier'],
			urls='https://en.wikipedia.org/wiki/List_of_aircraft_carriers',
			representation='list'
		)
	}

	military_vehicles = {
		'military_vehicles': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=progress_bar - 1, data_type=VEHICLE,
			categories=[VEHICLE, 'combat_vehicle', 'military_vehicle'],
			urls='https://en.wikipedia.org/wiki/List_of_U.S._military_vehicles_by_model_number',
			representation='list'
		)
	}

	cars1 = {
		'bmw_cars': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=progress_bar - 1, data_type=VEHICLE,
			categories=[VEHICLE, 'car', 'bmw'],
			urls='https://en.wikipedia.org/wiki/List_of_BMW_vehicles',
			representation='list',
			sections=['Cars']
		),
		'bmw_motorcycles': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=progress_bar - 1, data_type=VEHICLE,
			categories=[VEHICLE, 'motorcycle', 'bmw'],
			urls='https://en.wikipedia.org/wiki/List_of_BMW_vehicles',
			representation='list',
			sections=['Motorcycles']
		),
		'automobiles': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=progress_bar - 1, data_type=VEHICLE,
			categories=[VEHICLE, 'car'],
			urls=[
				'https://en.wikipedia.org/wiki/List_of_best-selling_automobiles',
				'https://en.wikipedia.org/wiki/List_of_automobile_sales_by_model'
			],
			representation='table',
			columns={VEHICLE: ['automobile']}
		),
		'toyota_cars': WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=progress_bar - 1, data_type=VEHICLE,
			categories=[VEHICLE, 'toyota', 'car'],
			urls='https://en.wikipedia.org/wiki/List_of_Toyota_vehicles',
			representation='table',
			columns={VEHICLE: ['model_2']}
		)
	}

	brands_and_urls = {
		'audi': 'https://en.wikipedia.org/wiki/List_of_Audi_vehicles',
		'austin': 'https://en.wikipedia.org/wiki/List_of_Austin_motor_vehicles',
		'ford': 'https://en.wikipedia.org/wiki/List_of_Ford_vehicles',
		'mercury': 'https://en.wikipedia.org/wiki/List_of_Mercury_vehicles',
		'moskvitch': 'https://en.wikipedia.org/wiki/List_of_Moskvitch_vehicles',
		'geo': 'https://en.wikipedia.org/wiki/List_of_Geo_vehicles',
		'buich': 'https://en.wikipedia.org/wiki/List_of_Buick_vehicles',
		'honda': 'https://en.wikipedia.org/wiki/List_of_Honda_automobiles',
		'chevrolet': 'https://en.wikipedia.org/wiki/List_of_Chevrolet_vehicles',
		'chrysler': 'https://en.wikipedia.org/wiki/List_of_Chrysler_vehicles',
		'diesel_car': 'https://en.wikipedia.org/wiki/List_of_diesel_automobiles',
		'dodge': 'https://en.wikipedia.org/wiki/List_of_Dodge_vehicles',
		'electric_car': [
			'https://en.wikipedia.org/wiki/List_of_electric_cars_currently_available',
			'https://en.wikipedia.org/wiki/List_of_production_battery_electric_vehicles_(table)'
		],
		'battery_electric_car': 'https://en.wikipedia.org/wiki/List_of_production_battery_electric_vehicles',
		'european_car': 'https://en.wikipedia.org/wiki/List_of_European_automobiles',
		'fast_car': 'https://en.wikipedia.org/wiki/List_of_fastest_production_cars_by_acceleration',
		'iran_khodro': 'https://en.wikipedia.org/wiki/List_of_Iran_Khodro_vehicles',
		'kia': 'https://en.wikipedia.org/wiki/List_of_Kia_Motors_automobiles',
		'lambodghini': 'https://en.wikipedia.org/wiki/List_of_Lamborghini_automobiles',
		'le_mans_prototype': 'https://en.wikipedia.org/wiki/List_of_Le_Mans_Prototypes',
		'lexus': 'https://en.wikipedia.org/wiki/List_of_Lexus_vehicles',
		'dacia': 'https://en.wikipedia.org/wiki/List_of_Dacia_vehicles',
		'gmc': 'https://en.wikipedia.org/wiki/List_of_GMC_vehicles',
		'hyundai': 'https://en.wikipedia.org/wiki/List_of_Hyundai_vehicles',
		'lincoln': 'https://en.wikipedia.org/wiki/List_of_Lincoln_vehicles',
		'van': 'https://en.wikipedia.org/wiki/List_of_vans',
		'maserati': 'https://en.wikipedia.org/wiki/List_of_Maserati_vehicles',
		'mazda': 'https://en.wikipedia.org/wiki/List_of_Mazda_vehicles',
		'mercedes_benz': 'https://en.wikipedia.org/wiki/List_of_Mercedes-Benz_vehicles',
		'oldsmobile': 'https://en.wikipedia.org/wiki/List_of_Oldsmobile_vehicles',
		'opel': 'https://en.wikipedia.org/wiki/List_of_Opel_vehicles',
		'packard': 'https://en.wikipedia.org/wiki/Packard#Packard_automobile_models',
		'plymouth': 'https://en.wikipedia.org/wiki/List_of_Plymouth_vehicles',
		'pontiac': 'https://en.wikipedia.org/wiki/List_of_Pontiac_vehicles',
		'porsche': 'https://en.wikipedia.org/wiki/List_of_Porsche_vehicles',
		'renault': 'https://en.wikipedia.org/wiki/List_of_Renault_vehicles',
		'saab': 'https://en.wikipedia.org/wiki/List_of_Saab_passenger_cars',
		'suv': 'https://en.wikipedia.org/wiki/List_of_sport_utility_vehicles',
		'sports_car': 'https://en.wikipedia.org/wiki/List_of_sports_cars',
		'vauxhall': 'https://en.wikipedia.org/wiki/List_of_Vauxhall_vehicles',
		'volkswagen': 'https://en.wikipedia.org/wiki/List_of_Volkswagen_passenger_vehicles',
		'volvo': 'https://en.wikipedia.org/wiki/List_of_Volvo_passenger_cars',
		'zil': 'https://en.wikipedia.org/wiki/List_of_ZiL_vehicles'
	}

	cars2 = {
		brand: WikipediaListGuide(
			list_type='list',
			wikipedia=wikipedia, echo=progress_bar - 1, data_type=VEHICLE,
			categories=[VEHICLE, 'car', brand],
			urls=url,
			columns={VEHICLE: ['name', 'model', 'model_name', 'car', 'vehicle_name_with_photograph', 'suv']},
			representation=None
		)
		for brand, url in brands_and_urls.items()
	}

	return WikipediaLists(
		echo=progress_bar,
		wikipedia_lists={
			**aircrafts, **ships, **military_vehicles, **cars1, **cars2
		}
	)