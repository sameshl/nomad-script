class Parameter:
	"""docstring for Paramerter"""
	def __init__(self, name):
		self.name = name

	def __str__(self):
		return "\tNAME : {}\n".format(self._name) 

class ProblemParameter(Parameter):
	"""docstring for ProblemParameter"""
	def __init__(self, name, input_type, lower_bound, upper_bound, default_value):
		Parameter.__init__(self, name)
		self.upper_bound = upper_bound
		self.lower_bound = lower_bound
		self.default_value = default_value
		self.input_type = input_type

	def __str__(self, name):
		string = Parameter.__str__(self, name)
		string = string + "\tMAX_VALUE : {}\n".format(self._max_value)
		string = string + "\tMIN_VALUE : {}\n".format(self._min_value)
		string = string + "\tVALUE : {}\n".format(self._value)
		string = string + "\tTYPE : {}\n".format(type(self._value))
		return string

class AlgorithmicParameter(Parameter):
	"""docstring for AlgorithmicParameter"""
	def __init__(self, name, config):
		Parameter.__init__(self, name)
		self.direction_type = config.dic['direction_type']
		self.f_target = config.dic['f_target']
		self.initial_mesh_size = config.dic['initial_mesh_size']
		self.lh_search = config.dic['lh_search']
		self.max_bb_eval = config.dic['max_bb_eval']
		self.max_time = config.dic['max_time']
		self.tmp_dir = config.dic['tmp_dir']

	def __str__(self, name):
		string = Parameter.__str__(self, name)
		string = string + "\t DIRECTION_TYPE : {}\n".format(self.direction_type)
		string = string + "\t F_TARGET : {}\n".format(self.f_target)
		string = string + "\t INITIAL_MESH_SIZE : {}\n".format(self.initial_mesh_size)
		string = string + "\t LH_SEARCH : {}\n".format(type(self.lh_search))
		string = string + "\t MAX_BB_EVAL : {}\n".format(self.max_bb_eval)
		string = string + "\t MAX_TIME : {}\n".format(self.max_time)
		string = string + "\t TMP_DIR : {}\n".format(self.tmp_dir)
		return string

class OutputParameter(Parameter):
	"""docstring for OutputParameter"""
	def __init__(self, name, config):
		Parameter.__init__(self, name)
		self.cache_file = config.dic['cache_file']
		self.display_all_eval = config.dic['display_all_eval']
		self.display_degree = config.dic['display_degree']
		self.display_stats = config.dic['display_stats']
		self.history_file = config.dic['history_file']
		self.solution_file = config.dic['solution_file']
		self.stats_file = config.dic['stats_file']

	def __str__(self, name):
		string = Parameter.__str__(self, name)
		string = string + "\t CACHE_FILE : {}\n".format(self.cache_file)
		string = string + "\t DISPLAY_ALL_EVAL : {}\n".format(self.display_all_eval)
		string = string + "\t DISPLAY_DEGREE : {}\n".format(self.display_degree)
		string = string + "\t DISPLAY_STATS : {}\n".format(self.display_stats)
		string = string + "\t HISTORY_FILE : {}\n".format(self.history_file)
		string = string + "\t SOLUTION_FILE : {}\n".format(self.solution_file)
		string = string + "\t STATS_FILE : {}\n".format(self.stats_file)
		return string
