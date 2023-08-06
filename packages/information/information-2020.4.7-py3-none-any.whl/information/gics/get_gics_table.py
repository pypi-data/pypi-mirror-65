from internet import Wikipedia


def get_text(x):
	try:
		return x.text
	except:
		return str(x)


def get_gics_table(url='https://en.wikipedia.org/wiki/Global_Industry_Classification_Standard', table_num=0):
	wikipedia = Wikipedia()
	page = wikipedia.get_page(url=url)
	table = page.tables[table_num].rename(columns={
		'sector_1': 'sector_code', 'sector_2': 'sector',
		'industry_group_1': 'industry_group_code', 'industry_group_2': 'industry_group',
		'industry_1': 'industry_code', 'industry_2': 'industry',
		'sub_industry_1': 'sub_industry_code', 'sub_industry_2': 'sub_industry'
	})
	for column in table.columns:
		table[column] = table[column].apply(func=get_text)
	return table


GICS_TABLE = get_gics_table()

def to_dict(df):
	return dict(sorted(df.values.tolist()))

SECTORS = to_dict(GICS_TABLE[['sector_code', 'sector']].drop_duplicates())
INDUSTRY_GROUPS = to_dict(GICS_TABLE[['industry_group_code', 'industry_group']].drop_duplicates())
INDUSTRIES = to_dict(GICS_TABLE[['industry_code', 'industry']].drop_duplicates())
SUB_INDUSTRIES = to_dict(GICS_TABLE[['sub_industry_code', 'sub_industry']].drop_duplicates())


def get_gics(code):
	code = str(code).ljust(8)
	sector = SECTORS.get(code[:2], None)
	industry_group = INDUSTRY_GROUPS.get(code[:4], sector)
	industry = INDUSTRIES.get(code[:6], industry_group)
	sub_industry = SUB_INDUSTRIES.get(code[:8], industry)
	return {
		'code': code, 'sector': sector, 'industry_group': industry_group,
		'industry': industry, 'sub_industry': sub_industry
	}
