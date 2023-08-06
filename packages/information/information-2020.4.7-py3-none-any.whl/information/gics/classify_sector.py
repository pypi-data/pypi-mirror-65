SECTOR_CLASSIFICATIONS = {
	'10': 'cyclical',  # energy  https://www.fool.com/investing/general/2012/09/20/the-basics-of-the-energy-sector.aspx
	'15': 'cyclical',  # materials https://www.fool.com/investing/general/2012/09/19/an-investors-guide-to-the-materials-sector.aspx
	'20': 'cyclical',  # industrials https://www.fool.com/investing/general/2012/09/19/the-basics-of-the-industrials-sector.aspx
	'25': 'sensitive',  # consumer discretionary https://marketrealist.com/2016/09/difference-consumer-discretionary-consumer-staples/
	'30': 'defensive',  # consumer staples https://www.thebalance.com/what-are-defensive-sectors-2466812
	'35': 'defensive',  # health care https://www.privatebanking.societegenerale.com/en/media/investment-strategy/equity-solutions/equity-nutshell/cyclical-defensive-stocks/
	'40': 'cyclical',  # financials https://fingerlakeswm.com/sector-investing-visualized/
	'45': 'sensitive',  # information technology https://www.investopedia.com/articles/stocks/10/primer-on-the-tech-industry.asp
	'50': 'cyclical',  # communication https://www.fidelity.com/bin-public/060_www_fidelity_com/documents/fidelity/sectors-are-shifting_fidelity.pdf
	'5010': 'defensive',  # telecom  https://www.fidelity.com/bin-public/060_www_fidelity_com/documents/fidelity/sectors-are-shifting_fidelity.pdf
	'55': 'defensive',  # utilities https://fingerlakeswm.com/sector-investing-visualized/
	'60': 'defensive'  # real estate https://www.thebalance.com/what-are-defensive-sectors-2466812
}


KEY_LENGTHS = sorted(list(set([len(key) for key in SECTOR_CLASSIFICATIONS.keys()])), reverse=True)


def classify_sector(gics):
	gics = str(gics)
	for key_length in KEY_LENGTHS:
		if len(gics) >= key_length:
			if gics[:key_length] in SECTOR_CLASSIFICATIONS:
				return SECTOR_CLASSIFICATIONS[gics[:key_length]]

	return 'unknown'
