from modules.tests.tests_suite import *

class test_object(dict):
	__getattr__= dict.__getitem__
	__setattr__= dict.__setitem__
	
	def __init__(self, test):
		self.test_name = test["test_name"]
		self.test_type = test["test_type"]
		self.test_url = global_dict["server"] + test["test_base_url"]
		self.test_function = test["test_function"]
		self.test_params = test["test_params"]
		
		try:
			self.test_repl = test["test_repl"]
		except:
			self.test_repl = ""
		
		try:
			self.test_headers = test["test_headers"]
		except:
			self.test_headers = ""

		self.test_expected = test["test_expected"]		
		
		try:
			self.output_mode = test["output_mode"]
		except:
			self.output_mode = 'w'	#default

		try:
			self.test_store = test["test_store"]
		except:
			self.test_store = ""
			
		self.actuals_folder = "" #will be filled in from main script
		self.data = "" #will be filled in from main script