import subprocess, re, io, os
from src.bb_parameters import *
from src.xml_manager import xmlCreator
from src.exceptions import BlackBoxException

class BlackBoxParser:
	"""docstring for BlackBoxParser"""
	def __init__(self, bb_path, bb_name, config):
		self.bb_path = bb_path
		self.bb_name = bb_name
		self.pb_params = []
		self.alg_params = []
		self.out_params = []
		self.output_types = []
		self.configuration = config
		self.instance_path = ""

		self.parse()
		self.addParameter(AlgorithmicParameter('default', self.configuration))
		self.addParameter(OutputParameter('default', self.configuration))

		if (self.configuration.dic['parameters_on_command_line'].lower() == "yes"):
			self.create_executable()

	def addParameter(self, value):
		if (value.__class__.__name__ == 'ProblemParameter'):
			self.pb_params.append(value)

		if (value.__class__.__name__ == 'AlgorithmicParameter'):
			self.alg_params.append(value)

		if (value.__class__.__name__ == 'OutputParameter'):
			self.out_params.append(value)

	def __len__(self):
		return len(self.pb_params)

	def parse(self):
		regex_input = '\s*(?P<name>\w*)\s+(?P<type>\w*)\s+(?P<min_value>[0-9.]+)\s+(?P<max_value>[0-9.]+)\s+(?P<value>[0-9.]+)'
		regex_instance = '^.*\s(.*.txt)$'
		regex_output = '^.*\s(NOTHING|-|OBJ|CNT_EVAL|EB|F|PB|CSTR|PEB|STAT_AVG|STAT_SUM)$'

		bb_param = subprocess.check_output(
			[self.bb_path + self.bb_name, '-param'], 
			universal_newlines=True)

		for line in io.StringIO(bb_param):
			param = re.compile(regex_input).search(line)
			instance = re.compile(regex_instance).search(line)
			output = re.compile(regex_output).search(line)

			if param:
				self.addParameter(ProblemParameter(
					param.group('name'),
					param.group('type'),
					param.group('min_value'),
					param.group('max_value'),
					param.group('value')))

			if instance:
				self.instance_path = instance.group(1)

			if output:
				self.output_types.append(output.group(1))


	def toxml(self, file_name):
		#problem parameters treatment
		lower_bounds = []
		upper_bounds = []
		input_types = []
		x0 = []

		xml_creator = xmlCreator()

		if (len(self) > 0):
			xml_creator.addParameter("DIMENSION", "problem", [len(self)])

		if (self.bb_path and self.bb_name):
			if (self.configuration.dic['parameters_on_command_line'].lower() == "yes"):
				xml_creator.addParameter("BB_EXE", "problem", [self.bb_path + "exe.py"])
			else:
				xml_creator.addParameter("BB_EXE", "problem", [self.bb_path + self.bb_name])

		for param in self.pb_params:
			lower_bounds.append(param.lower_bound)
			upper_bounds.append(param.upper_bound)
			input_types.append(convert_input_param(param.input_type))
			x0.append(param.default_value)

		if lower_bounds:
			xml_creator.addParameter("LOWER_BOUND", "problem", lower_bounds)
		else:
			raise BlackBoxException("lower_bounds")

		if upper_bounds:
			xml_creator.addParameter("UPPER_BOUND", "problem", upper_bounds)
		else:
			raise BlackBoxException("upper_bounds")

		if input_types:	
			xml_creator.addParameter("BB_INPUT_TYPE", "problem", input_types)
		else:
			raise BlackBoxException("input_types")

		if x0:
			xml_creator.addParameter("X0", "problem", x0)
		else:
			raise BlackBoxException("x0")

		if self.output_types:
			xml_creator.addParameter("BB_OUTPUT_TYPE", "problem", self.output_types)
		else:
			raise BlackBoxException("output_types")

		#output parameters treatment
		for alg_param in self.alg_params:
			if alg_param.direction_type:
				xml_creator.addParameter("DIRECTION_TYPE", "algorithmic", [alg_param.direction_type])

			if alg_param.f_target:
				xml_creator.addParameter("F_TARGET", "algorithmic", [alg_param.f_target])

			if alg_param.initial_mesh_size:
				xml_creator.addParameter("INITIAL_MESH_SIZE", "algorithmic", [alg_param.initial_mesh_size])

			if alg_param.lh_search:
				xml_creator.addParameter("LH_SEARCH", "algorithmic", [alg_param.lh_search])

			if alg_param.max_bb_eval:
				xml_creator.addParameter("MAX_BB_EVAL", "algorithmic", [alg_param.max_bb_eval])

			if alg_param.max_time:
				xml_creator.addParameter("MAX_TIME", "algorithmic", [alg_param.max_time])

			if alg_param.tmp_dir:
				xml_creator.addParameter("TMP_DIR", "algorithmic", [alg_param.tmp_dir])


		#algorithmic parameters treatment
		for out_param in self.out_params:
			if out_param.cache_file:
				xml_creator.addParameter("CACHE_FILE", "output", [out_param.cache_file])

			if out_param.display_all_eval:
				xml_creator.addParameter("DISPLAY_ALL_EVAL", "output", [out_param.display_all_eval])

			if out_param.display_degree:
				xml_creator.addParameter("DISPLAY_DEGREE", "output", [out_param.display_degree])

			if out_param.display_stats:
				xml_creator.addParameter("DISPLAY_STATS", "output", [out_param.display_stats])

			if out_param.history_file:
				xml_creator.addParameter("HISTORY_FILE", "output", [out_param.history_file])

			if out_param.solution_file:
				xml_creator.addParameter("SOLUTION_FILE", "output", [out_param.solution_file])

			if out_param.stats_file:
				xml_creator.addParameter("STATS_FILE", "output", [out_param.stats_file])

		#print(xml_creator)
		xml_creator.writexml(self.bb_path + file_name)

	def __str__(self):
		param_cpt = 0
		string = "PATH : {}\n".format(self.bb_path)
		string = string + "NAME : {}\n".format(
			self._bb_name)

		for param in self._params:
			param_cpt = param_cpt + 1
			string = string + "PARAMETER {} : \n{}".format(
				param_cpt,
				param.__str__())

		return string

	def create_executable(self):
		"""This function create an executable to execute the black box. DEPRECIATED"""
		file_string = "#!/usr/local/bin/python3.3\n# -*-coding:utf-8-*\n"
		file_string = file_string + "import argparse, os, sys\n"
		file_string = file_string + "if __name__ == \"__main__\":\n"
		file_string = file_string + "\tif (len(sys.argv) != 2):\n\t\tprint(\"Error\")\n"
		file_string = file_string + "\telif (len(sys.argv) == 2):\n\t\twith open(sys.argv[1], \"r\") as f:\n"
		file_string = file_string + "\t\t\tstring = \"\"\n\t\t\tfor line in f:\n"
		file_string = file_string + "\t\t\t\tword = line[:max(line.find(' '), 0) or None]\n"
		file_string = file_string + "\t\t\t\tstring = string + word + \" \"\n"
		file_string = file_string + "\t\t\tos.system(\"{0}{1} \" + string)\n".format(
			self.bb_path,
			self.bb_name)
		#print(file_string)

		exe_file = open(self.bb_path + "exe.py", "w")
		exe_file.write(file_string)
		os.system("chmod u+x " + self.bb_path + "exe.py")

def convert_input_param(string):
	if (re.search('i|I',string)):
		ret = 'I'
	elif (re.search('r|f|R|F', string)):
		ret = 'R'
	elif (re.search('c|C', string)):
		ret = 'C'
	elif (re.search('b|B', string)):
		ret = 'B'
	else:
		print("Invalid parameter !")

	return ret





