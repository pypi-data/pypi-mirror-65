from numpy import nan

class Country:
	def __init__(self, dictionary):
		"""
		:type dictionary: dict
		"""
		self._alpha_2 = None
		self._alpha_3 = None
		self._common_name = None
		self._name = None
		self._numeric = None
		self._official_name = None
		self._match_score = 0
		for k, v in dictionary.items():
			try:
				key = f'_{k}'
				if v is nan: v=None
				setattr(self, key, v)
			except:
				raise RuntimeError(f'cannot set key:"{key}" to value:"{v}"')
	@property
	def alpha2(self):
		return self._alpha_2

	code = alpha2

	@property
	def alpha3(self):
		return self._alpha_3

	@property
	def common_name(self):
		return self._common_name

	@property
	def name(self):
		return self._name

	@property
	def numeric(self):
		return self._numeric

	@property
	def official_name(self):
		return self._official_name

	@property
	def match_score(self):
		return self._match_score

	def __repr__(self):
		return str(self)

	def __str__(self):
		return f'Country: {self.name} [{self.code}] [{self.match_score}]'


