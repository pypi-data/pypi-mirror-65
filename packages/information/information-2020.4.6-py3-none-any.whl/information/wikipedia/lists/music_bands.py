from ..WikipediaListGuide import WikipediaListGuide
from ..WikipediaLists import WikipediaLists
from chronometry.progress import ProgressBar

BAND = 'artist_or_band'
ALBUM = 'album'


def get_music_bands(wikipedia=None, echo=0):
	urls_and_categories = [
		('https://en.wikipedia.org/wiki/List_of_American_grunge_bands', ['pop_rock', 'american_grunge']),
		('https://en.wikipedia.org/wiki/List_of_anarcho-punk_bands', ['pop_rock', 'punk_rock', 'anarchist_punk']),
		('https://en.wikipedia.org/wiki/List_of_music_artists_and_bands_from_Argentina', ['argentine']),
		('https://en.wikipedia.org/wiki/List_of_bands_from_the_San_Francisco_Bay_Area', ['american', 'san_franciscan']),
		('https://en.wikipedia.org/wiki/List_of_Belarusian_musical_groups', ['belarusian']),
		('https://en.wikipedia.org/wiki/List_of_music_artists_and_bands_from_England', ['british']),
		('https://en.wikipedia.org/wiki/List_of_bands_from_British_Columbia', ['canadian', 'british_columbian']),
		('https://en.wikipedia.org/wiki/List_of_British_Invasion_artists', ['pop_rock', 'british_invasion']),
		(
			'https://en.wikipedia.org/wiki/List_of_Chicago_hardcore_punk_bands',
			['pop_rock', 'punk_rock', 'hardcore_punk', 'chicagoan']
		),
		(
			'https://en.wikipedia.org/wiki/List_of_Christian_hardcore_bands',
			['pop_rock', 'punk_rock', 'hardcore_punk', 'christian_hardcore_punk', 'christian_music']
		),
		(
			'https://en.wikipedia.org/wiki/List_of_Christian_rock_bands',
			['pop_rock', 'christian_rock', 'christian_music']
		),
		('https://en.wikipedia.org/wiki/List_of_bands_that_played_at_Dagenham_Roundhouse', []),
		('https://en.wikipedia.org/wiki/List_of_bands_from_Delhi', ['indian', 'delhiite']),
		('https://en.wikipedia.org/wiki/List_of_emo_artists', ['pop_rock', 'emo', 'punk_rock']),
		('https://en.wikipedia.org/wiki/List_of_experimental_big_bands', ['jazz', 'big_band', 'experimental_big_band']),
		('https://en.wikipedia.org/wiki/List_of_extreme_metal_bands', ['pop_rock', 'heavy_metal', 'extreme_metal']),
		('https://en.wikipedia.org/wiki/List_of_all-female_bands', ['all_female_band']),
		('https://en.wikipedia.org/wiki/List_of_girl_groups', ['girl_group']),
		('https://en.wikipedia.org/wiki/List_of_bands_from_Glasgow', ['glaswegians']),
		('https://en.wikipedia.org/wiki/List_of_bands_from_Gothenburg', ['gothenburgian']),
		('https://en.wikipedia.org/wiki/List_of_grunge_bands', ['pop_rock', 'grunge']),
		('https://en.wikipedia.org/wiki/List_of_hardcore_punk_bands', ['pop_rock', 'punk_rock', 'hardcore_punk']),
		('https://en.wikipedia.org/wiki/List_of_instrumental_bands', ['instrumental']),
		('https://en.wikipedia.org/wiki/List_of_jam_bands', ['jam_band']),
		('https://en.wikipedia.org/wiki/List_of_Klezmer_bands', ['klezmer_band']),
		('https://en.wikipedia.org/wiki/List_of_bands_from_Lincoln,_Nebraska', ['american', 'nebraskan']),
		('https://en.wikipedia.org/wiki/List_of_bands_from_Los_Angeles', ['american', 'angeleno']),
		('https://en.wikipedia.org/wiki/List_of_musical_supergroups', ['musical_supergroup']),
		(
			'https://en.wikipedia.org/wiki/List_of_punk_bands_from_the_United_Kingdom',
			['pop_rock', 'punk_rock', 'british']
		),
		(
			[
				'https://en.wikipedia.org/wiki/List_of_punk_rock_bands,_0%E2%80%93K',
				'https://en.wikipedia.org/wiki/List_of_punk_rock_bands,_L%E2%80%93Z',
				'https://en.wikipedia.org/wiki/List_of_1970s_punk_rock_musicians',
				'https://en.wikipedia.org/wiki/List_of_musicians_in_the_second_wave_of_punk_rock'
			],
			['pop_rock', 'punk_rock']
		),
		('https://en.wikipedia.org/wiki/List_of_music_artists_and_bands_from_Manchester', ['british', 'mancunian']),
		('https://en.wikipedia.org/wiki/List_of_bands_and_artists_from_Merseyside', ['british']),
		('https://en.wikipedia.org/wiki/List_of_music_artists_and_bands_from_Mexico', ['mexican']),
		('https://en.wikipedia.org/wiki/List_of_band_name_etymologies', []),
		('https://en.wikipedia.org/wiki/List_of_bands_named_after_other_performers%27_songs', []),
		('https://en.wikipedia.org/wiki/List_of_bands_formed_in_New_York_City', ['american', 'new_yorker']),
		('https://en.wikipedia.org/wiki/List_of_musical_artists_from_New_Zealand', ['kiwi']),
		('https://en.wikipedia.org/wiki/List_of_original_names_of_bands', []),
		('https://en.wikipedia.org/wiki/List_of_Philippine-based_music_groups', ['filipino']),
		('https://en.wikipedia.org/wiki/List_of_pipe_bands', ['pipe_band']),
		('https://en.wikipedia.org/wiki/List_of_post-punk_bands', ['pop_rock', 'punk_rock', 'post_punk']),
		('https://en.wikipedia.org/wiki/List_of_power_trios', ['pop_rock', 'power_trio']),
		('https://en.wikipedia.org/wiki/List_of_riot_grrrl_bands', ['pop_rock', 'punk_rock', 'riot_grrrl']),
		('https://en.wikipedia.org/wiki/List_of_screamo_bands', ['pop_rock', 'punk_rock', 'screamo']),
		('https://en.wikipedia.org/wiki/List_of_bands_from_Spain', ['spanish']),
		('https://en.wikipedia.org/wiki/List_of_straight_edge_bands', ['pop_rock', 'punk_rock', 'straight_edge']),
		('https://en.wikipedia.org/wiki/List_of_bands_from_Taiwan', ['taiwanese']),
		('https://en.wikipedia.org/wiki/List_of_visual_kei_musical_groups', ['visual_kei_musical_group']),
		('https://en.wikipedia.org/wiki/List_of_progressive_rock_artists', ['pop_rock', 'progressive_rock']),
		('https://en.wikipedia.org/wiki/List_of_heavy_metal_bands', ['pop_rock', 'heavy_metal']),
		(
			[
				'https://en.wikipedia.org/wiki/List_of_black_metal_bands,_0%E2%80%93K',
				'https://en.wikipedia.org/wiki/List_of_black_metal_bands,_L%E2%80%93Z'
			],
			['pop_rock', 'black_metal']
		),
		('https://en.wikipedia.org/wiki/List_of_acid_rock_artists', ['pop_rock', 'acid_rock']),
		('https://en.wikipedia.org/wiki/List_of_new-age_music_artists', ['new_age']),
		('https://en.wikipedia.org/wiki/List_of_thrash_metal_bands', ['pop_rock', 'heavy_metal', 'thrash_metal']),
		('https://en.wikipedia.org/wiki/List_of_speed_metal_bands', ['pop_rock', 'heavy_metal', 'speed_metal']),
		('https://en.wikipedia.org/wiki/List_of_industrial_metal_bands', ['pop_rock', 'industrial_metal']),
		('https://en.wikipedia.org/wiki/List_of_alternative_rock_artists', ['pop_rock', 'alternative_pop_rock']),
		('https://en.wikipedia.org/wiki/List_of_adult_alternative_artists', ['pop_rock', 'adult_alternative_pop_rock']),
		('https://en.wikipedia.org/wiki/List_of_soft_rock_artists_and_songs', ['pop_rock', 'soft_rock']),
		('https://en.wikipedia.org/wiki/Adult_Contemporary_(chart)', ['pop_rock', 'soft_rock', 'adult_contemporary']),
		('https://en.wikipedia.org/wiki/List_of_dream_pop_artists', ['pop_rock', 'alternative_pop_rock', 'dream_pop']),
		('https://en.wikipedia.org/wiki/List_of_synth-pop_artists', ['pop_rock', 'synth_pop']),
		('https://en.wikipedia.org/wiki/List_of_southern_rock_bands', ['pop_rock', 'southern_rock']),
		('https://en.wikipedia.org/wiki/List_of_folk_rock_artists', ['pop_rock', 'folk_rock']),
		(
			[
				'https://en.wikipedia.org/wiki/List_of_country_performers_by_era',
				'https://en.wikipedia.org/wiki/List_of_artists_who_reached_number_one_on_the_U.S._country_chart'
			],
			['country']
		),
		(
			'https://en.wikipedia.org/wiki/List_of_Christian_country_artists',
			['country', 'christian_country', 'christian_music']
		),
		('https://en.wikipedia.org/wiki/List_of_blues_rock_musicians', ['pop_rock', 'blues_rock']),
		('https://en.wikipedia.org/wiki/List_of_blues_musicians', ['blues']),
		('https://en.wikipedia.org/wiki/List_of_best-selling_music_artists', ['best_selling_artist']),
		('https://en.wikipedia.org/wiki/List_of_Eurobeat_artists', ['eurobeat']),
		(
			[
				'https://en.wikipedia.org/wiki/List_of_disco_artists_(A%E2%80%93E)',
				'https://en.wikipedia.org/wiki/List_of_disco_artists_(F%E2%80%93K)',
				'https://en.wikipedia.org/wiki/List_of_disco_artists_(L%E2%80%93R)',
				'https://en.wikipedia.org/wiki/List_of_disco_artists_(S%E2%80%93Z)'
			],
			['disco']
		),
		('https://en.wikipedia.org/wiki/List_of_dance-pop_artists', ['dance_pop']),
		('https://en.wikipedia.org/wiki/List_of_alternative_hip_hop_artists', ['hip_hop', 'alternative_hip_hop']),
		('https://en.wikipedia.org/wiki/List_of_Christian_hip_hop_artists', ['hip_hop', 'christian_hip_hop']),
		('https://en.wikipedia.org/wiki/List_of_gothic_rock_artists', ['pop_rock', 'gothic_rock']),
		('https://en.wikipedia.org/wiki/List_of_electronic_rock_artists', ['pop_rock', 'electronic_rock']),
		('https://en.wikipedia.org/wiki/List_of_1970s_Christian_pop_artists', ['christian_pop']),
		('https://en.wikipedia.org/wiki/List_of_alternative_country_musicians', ['country', 'alternative_country']),
		(
			'https://en.wikipedia.org/wiki/List_of_alternative_metal_artists',
			['pop_rock', 'heavy_metal', 'alternative_metal']
		),
		('https://en.wikipedia.org/wiki/List_of_baroque_pop_artists', ['baroque_pop']),
		('https://en.wikipedia.org/wiki/List_of_bebop_musicians', ['bepop']),
		('https://en.wikipedia.org/wiki/List_of_bhangra_artists', ['bhangra']),
		('https://en.wikipedia.org/wiki/List_of_big_band_musicians', ['big_band']),
		('https://en.wikipedia.org/wiki/List_of_blue-eyed_soul_artists', ['soul', 'blue_eyed_soul']),
		('https://en.wikipedia.org/wiki/List_of_bluegrass_musicians', ['blue_grass']),
		('https://en.wikipedia.org/wiki/List_of_C-pop_artists', ['pop_rock', 'c_pop']),
		('https://en.wikipedia.org/wiki/List_of_calypso_musicians', ['calypso']),
		('https://en.wikipedia.org/wiki/List_of_Celtic_musicians', ['celtic']),
		('https://en.wikipedia.org/wiki/List_of_chamber_jazz_musicians', ['jazz', 'chamber_jazz']),
		('https://en.wikipedia.org/wiki/List_of_Chicago_blues_musicians', ['blues', 'chicago_blues']),
		(
			'https://en.wikipedia.org/wiki/List_of_Christian_dance,_electronic,_and_techno_artists',
			['christian_music', 'christian_electronic']
		),
		(
			'https://en.wikipedia.org/wiki/List_of_Christian_metal_artists',
			['pop_rock', 'heavy_metal', 'christian_metal', 'christian_music']
		),
		('https://en.wikipedia.org/wiki/List_of_dance-punk_artists', ['dance_punk']),
		('https://en.wikipedia.org/wiki/List_of_dance-rock_artists', ['pop_rock', 'dance_rock']),
		('https://en.wikipedia.org/wiki/List_of_dark_ambient_artists', ['dark_ambient']),
		('https://en.wikipedia.org/wiki/List_of_dark_cabaret_artists', ['dark_cabaret']),
		('https://en.wikipedia.org/wiki/List_of_dark_rock_bands', ['pop_rock', 'dark_rock']),
		(
			[
				'https://en.wikipedia.org/wiki/List_of_death_metal_bands,_!%E2%80%93K',
				'https://en.wikipedia.org/wiki/List_of_death_metal_bands,_L%E2%80%93Z'
			],
			['pop_rock', 'heavy_metal', 'death_metal']
		),
		('https://en.wikipedia.org/wiki/List_of_deathcore_artists', ['pop_rock', 'heavy_metal', 'deathcore']),
		('https://en.wikipedia.org/wiki/List_of_Delta_blues_musicians', ['blues', 'delta_blues']),
		('https://en.wikipedia.org/wiki/List_of_electric_blues_musicians', ['blues', 'electric_blues']),
		('https://en.wikipedia.org/wiki/List_of_electro_house_artists', ['electro_house']),
		('https://en.wikipedia.org/wiki/List_of_electro-industrial_bands', ['electro_industrial']),
		('https://en.wikipedia.org/wiki/List_of_electroclash_bands_and_artists', ['electroclash']),
		('https://en.wikipedia.org/wiki/List_of_fado_musicians', ['fado']),
		('https://en.wikipedia.org/wiki/List_of_folk_musicians', ['folk']),
		('https://en.wikipedia.org/wiki/List_of_folk_metal_bands', ['pop_rock', 'heavy_metal', 'folk_metal']),
		('https://en.wikipedia.org/wiki/List_of_G-funk_musicians', ['g_funk']),
		('https://en.wikipedia.org/wiki/List_of_gangsta_rap_artists', ['gangsta_rap']),
		('https://en.wikipedia.org/wiki/List_of_garage_rock_bands', ['pop_rock', 'garage_rock']),
		(
			'https://en.wikipedia.org/wiki/List_of_glam_metal_bands_and_artists',
			['pop_rock', 'heavy_metal', 'glam_metal']
		),
		('https://en.wikipedia.org/wiki/List_of_glam_punk_artists', ['pop_rock', 'punk_rock', 'glam_punk']),
		('https://en.wikipedia.org/wiki/List_of_glam_rock_artists', ['pop_rock', 'glam_rock']),
		(
			[
				'https://en.wikipedia.org/wiki/List_of_hard_rock_musicians_(A%E2%80%93M)',
				'https://en.wikipedia.org/wiki/List_of_hard_rock_musicians_(N%E2%80%93Z)'
			],
			['pop_rock', 'hard_rock']
		),
		('https://en.wikipedia.org/wiki/List_of_indie_pop_artists', ['indie_pop']),
		('https://en.wikipedia.org/wiki/List_of_indie_rock_musicians', ['pop_rock', 'indie_rock']),
		('https://en.wikipedia.org/wiki/List_of_Indonesian_pop_musicians', ['indonesian_pop']),
		('https://en.wikipedia.org/wiki/List_of_J-pop_artists', ['j_pop']),
		('https://en.wikipedia.org/wiki/List_of_Japanoise_artists', ['japanoise']),
		('https://en.wikipedia.org/wiki/List_of_jazz_fusion_musicians', ['jazz', 'jazz_fusion']),
		('https://en.wikipedia.org/wiki/List_of_K-pop_artists', ['k_pop']),
		('https://en.wikipedia.org/wiki/List_of_Latin_American_rock_musicians', ['pop_rock', 'latin_american', 'rock']),
		('https://en.wikipedia.org/wiki/List_of_Latin_pop_artists', ['latin_pop']),
		('https://en.wikipedia.org/wiki/List_of_maritime_music_performers', ['maritime_music']),
		('https://en.wikipedia.org/wiki/List_of_math_rock_groups', ['pop_rock', 'math_rock']),
		('https://en.wikipedia.org/wiki/List_of_mathcore_bands', ['mathcore']),
		('https://en.wikipedia.org/wiki/List_of_merengue_musicians', ['merengue_music']),
		('https://en.wikipedia.org/wiki/List_of_new_jack_swing_artists', ['new_jack_swing']),
		('https://en.wikipedia.org/wiki/List_of_new_wave_artists', ['new_wave']),
		('https://en.wikipedia.org/wiki/List_of_Oi!_bands', ['pop_rock', 'punk_rock', 'oi_band']),
		('https://en.wikipedia.org/wiki/List_of_Piedmont_blues_musicians', ['blues', 'piedmont_blues']),
		('https://en.wikipedia.org/wiki/List_of_political_hip_hop_artists', ['hip_hop', 'political_hip_hop']),
		('https://en.wikipedia.org/wiki/List_of_polka_artists', ['polka']),
		('https://en.wikipedia.org/wiki/List_of_pop_punk_bands', ['pop_punk']),
		('https://en.wikipedia.org/wiki/List_of_post-disco_artists_and_songs', ['post_disco']),
		('https://en.wikipedia.org/wiki/List_of_post-dubstep_musicians', ['post_dubstep']),
		('https://en.wikipedia.org/wiki/List_of_post-grunge_bands', ['pop_rock', 'post_grunge']),
		('https://en.wikipedia.org/wiki/List_of_post-hardcore_bands', ['pop_rock', 'punk_rock', 'post_hardcore']),
		('https://en.wikipedia.org/wiki/Post-metal', ['pop_rock', 'heavy_metal', 'post_metal']),
		('https://en.wikipedia.org/wiki/List_of_post-punk_revival_bands', ['pop_rock', 'punk_rock', 'post_punk_revival']),
		('https://en.wikipedia.org/wiki/List_of_post-rock_bands', ['pop_rock', 'post_rock']),
		('https://en.wikipedia.org/wiki/List_of_power_metal_bands', ['pop_rock', 'heavy_metal', 'power_metal']),
		('https://en.wikipedia.org/wiki/List_of_power_pop_artists_and_songs', ['power_pop']),
		('https://en.wikipedia.org/wiki/List_of_R%26B_musicians', ['rhythm_and_blues']),
		('https://en.wikipedia.org/wiki/List_of_ragtime_musicians', ['ragtime']),
		('https://en.wikipedia.org/wiki/List_of_ra%C3%AF_musicians', ['rai']),
		('https://en.wikipedia.org/wiki/List_of_rap_rock_bands', ['rap_rock']),
		('https://en.wikipedia.org/wiki/List_of_reggae_musicians', ['reggae']),
		('https://en.wikipedia.org/wiki/List_of_reggae_fusion_artists', ['reggae', 'reggae_fusion']),
		('https://en.wikipedia.org/wiki/List_of_reggae_rock_artists', ['reggae', 'reggae_rock']),
		('https://en.wikipedia.org/wiki/List_of_shoegazing_musicians', ['pop_rock', 'alternative_pop_rock', 'shoegazing']),
		('https://en.wikipedia.org/wiki/List_of_ska_musicians', ['ska']),
		('https://en.wikipedia.org/wiki/List_of_smooth_jazz_musicians', ['jazz', 'smooth_jazz']),
		('https://en.wikipedia.org/wiki/List_of_soul_musicians', ['soul']),
		('https://en.wikipedia.org/wiki/List_of_soul-blues_musicians', ['blues', 'soul_blues']),
		('https://en.wikipedia.org/wiki/List_of_technical_death_metal_bands', ['pop_rock', 'heavy_metal', 'death_metal', 'technical_death_metal']),
		('https://en.wikipedia.org/wiki/List_of_Texas_blues_musicians', ['blues', 'texas_blues']),
		('https://en.wikipedia.org/wiki/List_of_Thai_pop_artists', ['thai_pop']),
		('https://en.wikipedia.org/wiki/List_of_UK_garage_artists', ['electronic_music', 'uk_garage']),
		('https://en.wikipedia.org/wiki/List_of_Viking_metal_bands', ['pop_rock', 'heavy_metal', 'viking_metal']),
		('https://en.wikipedia.org/wiki/List_of_West_Coast_blues_musicians', ['blues', 'west_coast_blues']),
		('https://en.wikipedia.org/wiki/List_of_ambient_music_artists', ['ambient_music']),
		('https://en.wikipedia.org/wiki/List_of_Arabic_pop_musicians', ['arabic_pop']),
		('https://en.wikipedia.org/wiki/List_of_boogie_woogie_musicians', ['boogie_woogie']),
		('https://en.wikipedia.org/wiki/List_of_British_blues_musicians', ['blues', 'british_blues']),
		('https://en.wikipedia.org/wiki/List_of_Britpop_musicians', ['pop_rock', 'britpop']),
		('https://en.wikipedia.org/wiki/List_of_Christian_ska_bands', ['pop_rock', 'ska', 'christian_ska', 'christian_music']),
		('https://en.wikipedia.org/wiki/List_of_classic_female_blues_singers', ['blues', 'classic_female_blues']),
		('https://en.wikipedia.org/wiki/List_of_cool_jazz_and_West_Coast_jazz_musicians', ['jazz', 'cool_jazz']),
		('https://en.wikipedia.org/wiki/List_of_country_blues_musicians', ['blues', 'country_blues']),
		('https://en.wikipedia.org/wiki/List_of_country_music_performers', ['country']),
		('https://en.wikipedia.org/wiki/List_of_country_rock_musicians', ['country_rock']),
		('https://en.wikipedia.org/wiki/List_of_crooners', ['crooner']),
		(
			[
				'https://en.wikipedia.org/wiki/List_of_disco_artists_(A%E2%80%93E)',
				'https://en.wikipedia.org/wiki/List_of_disco_artists_(F%E2%80%93K)',
				'https://en.wikipedia.org/wiki/List_of_disco_artists_(L%E2%80%93R)',
				'https://en.wikipedia.org/wiki/List_of_disco_artists_(S%E2%80%93Z)'
			],
			['disco']
		),
		('https://en.wikipedia.org/wiki/List_of_doo-wop_musicians', ['doo_wop']),
		('https://en.wikipedia.org/wiki/List_of_doom_metal_bands', ['pop_rock', 'heavy_metal', 'doom_metal']),
		('https://en.wikipedia.org/wiki/List_of_downtempo_artists', ['electronic_music', 'downtempo']),
		('https://en.wikipedia.org/wiki/List_of_drone_artists', ['drone_music']),
		('https://en.wikipedia.org/wiki/List_of_dub_artists', ['reggae', 'dub_music', 'electronic_music']),
		('https://en.wikipedia.org/wiki/List_of_dubstep_musicians', ['electronic_music', 'dance_music', 'dubstep']),
		('https://en.wikipedia.org/wiki/List_of_Euro_disco_artists', ['dance_music', 'euro_disco']),
		('https://en.wikipedia.org/wiki/List_of_Eurobeat_artists', ['dance_music', 'eurobeat']),
		('https://en.wikipedia.org/wiki/List_of_Eurodance_artists', ['dance_music', 'eurodance']),
		('https://en.wikipedia.org/wiki/List_of_Europop_artists', ['europop']),
		('https://en.wikipedia.org/wiki/List_of_free_funk_musicians', ['jazz', 'fusion', 'free_funk']),
		('https://en.wikipedia.org/wiki/List_of_funk_musicians', ['rhythm_and_blues', 'soul', 'funk']),
		('https://en.wikipedia.org/wiki/List_of_funk_rock_bands', ['pop_rock', 'funk_rock']),
		('https://en.wikipedia.org/wiki/List_of_gospel_blues_musicians', ['blues', 'gospel_blues']),
		('https://en.wikipedia.org/wiki/List_of_gospel_musicians', ['gospel']),
		('https://en.wikipedia.org/wiki/List_of_gothic_metal_bands', ['pop_rock', 'heavy_metal', 'gothic_metal']),
		('https://en.wikipedia.org/wiki/List_of_grindcore_bands', ['pop_rock', 'heavy_metal', 'punk_rock', 'grindcore']),
		('https://en.wikipedia.org/wiki/List_of_groove_metal_bands', ['pop_rock', 'heavy_metal', 'groove_metal']),
		(
			[
				'https://en.wikipedia.org/wiki/List_of_hip_hop_groups',
				'https://en.wikipedia.org/wiki/List_of_hip_hop_musicians'
			],
			['hip_hop']
		),
		('https://en.wikipedia.org/wiki/List_of_horror_punk_bands', ['pop_rock', 'punk_rock', 'horror_punk']),
		('https://en.wikipedia.org/wiki/List_of_house_music_artists', ['dance_music', 'house_music']),
		('https://en.wikipedia.org/wiki/List_of_industrial_music_bands', ['industrial_music']),
		('https://en.wikipedia.org/wiki/List_of_intelligent_dance_music_artists', ['electronic_music', 'intelligent_dance']),
		('https://en.wikipedia.org/wiki/List_of_Italo_disco_artists_and_songs', ['disco', 'italo_disco']),
		('https://en.wikipedia.org/wiki/List_of_jazz_musicians', ['jazz']),
		('https://en.wikipedia.org/wiki/List_of_jump_blues_musicians', ['blues', 'jump_blues']),
		('https://en.wikipedia.org/wiki/List_of_jungle_and_drum_and_bass_artists', ['jungle_and_drum_and_bass', 'electronic_music']),
		('https://en.wikipedia.org/wiki/List_of_klezmer_musicians', ['klezmer']),
		('https://en.wikipedia.org/wiki/List_of_lovers_rock_artists', ['reggae', 'lovers_rock']),
		('https://en.wikipedia.org/wiki/List_of_metalcore_bands', ['pop_rock', 'heavy_metal', 'metalcore']),
		('https://en.wikipedia.org/wiki/List_of_melodic_death_metal_bands', ['pop_rock', 'heavy_metal', 'melodic_death_metal']),
		('https://en.wikipedia.org/wiki/List_of_new_wave_of_British_heavy_metal_bands', ['pop_rock', 'heavy_metal', 'new_wave_of_british_metal']),
		('https://en.wikipedia.org/wiki/List_of_noise_musicians', ['noise_music']),
		('https://en.wikipedia.org/wiki/List_of_nu_metal_bands', ['pop_rock', 'heavy_metal', 'alternative_metal', 'nu_metal']),
		('https://en.wikipedia.org/wiki/List_of_progressive_house_artists', ['house_music', 'progressive_house']),
		('https://en.wikipedia.org/wiki/List_of_progressive_metal_artists', ['pop_rock', 'heavy_metal', 'progressive_metal']),
		('https://en.wikipedia.org/wiki/List_of_progressive_rock_supergroups', ['progressive_rock', 'supergroup']),
		('https://en.wikipedia.org/wiki/List_of_psychedelic_folk_artists', ['folk', 'psychedelic', 'psychedelic_folk']),
		('https://en.wikipedia.org/wiki/List_of_psychedelic_pop_artists', ['psychedelic', 'psychedelic_pop']),
		('https://en.wikipedia.org/wiki/List_of_psychedelic_rock_artists', ['psychedelic', 'psychedelic_rock']),
		('https://en.wikipedia.org/wiki/List_of_psychobilly_bands', ['pop_rock', 'punk_rock', 'psychobilly']),
		('https://en.wikipedia.org/wiki/List_of_punk_blues_musicians_and_bands', ['pop_rock', 'punk_rock', 'punk_blues']),
		('https://en.wikipedia.org/wiki/List_of_reggaeton_musicians', ['reggaeton']),
		('https://en.wikipedia.org/wiki/List_of_rock_music_performers', ['pop_rock', 'rock']),
		('https://en.wikipedia.org/wiki/List_of_rocksteady_musicians', ['rocksteady']),
		('https://en.wikipedia.org/wiki/List_of_roots_reggae_artists', ['reggae', 'roots_reggae']),
		('https://en.wikipedia.org/wiki/List_of_roots_rock_bands_and_musicians', ['pop_rock', 'roots_rock']),
		('https://en.wikipedia.org/wiki/List_of_soul_jazz_musicians', ['jazz', 'soul_jazz']),
		('https://en.wikipedia.org/wiki/List_of_street_punk_bands', ['punk_rock', 'street_punk']),
		('https://en.wikipedia.org/wiki/List_of_surf_musicians', ['pop_rock', 'surf_music']),
		('https://en.wikipedia.org/wiki/List_of_swing_musicians', ['swing']),
		('https://en.wikipedia.org/wiki/List_of_symphonic_metal_bands', ['pop_rock', 'heavy_metal', 'symphonic_metal']),
		('https://en.wikipedia.org/wiki/Thrashcore', ['pop_rock', 'punk_rock', 'thrashcore']),
		('https://en.wikipedia.org/wiki/List_of_trip_hop_artists', ['trip_hop']),
		('https://en.wikipedia.org/wiki/List_of_vocal_groups', ['vocal_group']),
		('https://en.wikipedia.org/wiki/List_of_vocal_trance_artists', ['electronic_music', 'trance', 'vocal_trance']),
		('https://en.wikipedia.org/wiki/List_of_West_Coast_hip_hop_artists', ['hip_hop', 'west_coast'])

	]

	echo = max(0, echo)
	progress_bar = ProgressBar(echo=echo, total=None)

	return WikipediaLists(
		wikipedia_lists={
			(urls[0] if isinstance(urls, list) else urls): WikipediaListGuide(
				list_type='list',
				wikipedia=wikipedia, echo=progress_bar - 1, data_type=BAND, categories=[BAND] + categories, urls=urls,
				columns={
					BAND: ['band', 'band_project_name', 'band_name', 'name', 'artist', 'project_name', 'artist_name']
				}
			)
			for urls, categories in urls_and_categories
		},
		echo=progress_bar
	)
