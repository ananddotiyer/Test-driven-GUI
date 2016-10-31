#!/usr/bin/env python

#import requests
#import ast
#import json
import re
import sys
import traceback

from importlib import import_module
from modules.tests.tests_suite import *
from modules.libraries.verification import *
from modules.libraries.test_object import *

global_dict["debuglog"] = open(global_dict["debuglog"] + "debuglog.txt",'w')
global_dict["reslog"]  = open(global_dict["reslog"] + "passfaillog.csv",'w')

report_start ()

for tests in tests_suite:
	subfolder = ""
	tests_in_folder = tests.split ('.')

	#import only the required list of tests; contained in test_list
	mod = import_module ("modules.tests." + tests)
	if len(tests_in_folder) > 1:
		for folder in tests_in_folder[:-1]:
			subfolder += "\\" + folder
		tests = tests_in_folder[-1]
		subfolder += "\\"
	
	test_list = getattr (mod, tests)
	
	for test in test_list:
		global current_test
		current_test = test_object(test)
		
		#Execute only the test_types in run_list (tests_suite.py)
		if not current_test.test_type in run_list:
			continue
		
		#substitute for test_store
		try:
			test_store = current_test.test_store
			for each_key in current_test.keys():
				if each_key == "test_store":
					continue
				
				if isinstance (current_test[each_key], dict):
					for each_subkey in current_test[each_key].keys():
						if isinstance (current_test[each_key][each_subkey], int):
							continue
						
						#Replace anything between <> from global_dict						
						matchIt = re.compile ("<(.*)>")
						MatchObject = matchIt.search (current_test[each_key][each_subkey])
						if MatchObject:
							for groupItem in MatchObject.groups(1):
								current_test[each_key][each_subkey] = matchIt.sub(global_dict[groupItem], current_test[each_key][each_subkey])
				else:
					#Replace anything between <> from global_dict						
					matchIt = re.compile ("<(.*)>")
					MatchObject = matchIt.search (current_test[each_key])
					if MatchObject:
						for groupItem in MatchObject.groups(1):
							current_test[each_key] = matchIt.sub(global_dict[groupItem], current_test[each_key])
		except:
			traceback.print_exc (file=global_dict["debuglog"]) #test_store may not be present

		#Store object attributes temporarily, before using them
		test_url = current_test.test_url
		test_type = current_test.test_type
		test_name = current_test.test_name
		test_function = current_test.test_function
		test_params = current_test.test_params
		test_headers = current_test.test_headers
		test_expected = current_test.test_expected
		output_mode = current_test.output_mode
		
		#get the function pointer
		mod = import_module ("modules.libraries." + test_type + ".test_functions")
		function_to_call = getattr (mod, test_function)

		#substituting for the test_repl
		old_test_url = test_url
		try:
			url_placeholders = current_test.test_repl.values()
			
			combinations = [[]]
			for url_placeholder in url_placeholders:
					combination = []
					for j in url_placeholder:
						for i in combinations:
							combination.append(i+[j])
					combinations = combination
		
			print combinations

			items_to_replace = current_test.test_repl.keys()
			for combination in combinations:
				index = 0
				result = False
				test_url = old_test_url
				for item in items_to_replace:
						matchIt = re.compile ("{" + item + "}")
						test_url = matchIt.sub(combination[index], test_url)
						index += 1
						
				current_test.test_url = test_url #replace in the test_object
				actuals_folder = global_dict["actuals_folder"] + subfolder + "actuals\\" + test_name #re-using for writing the reports.
				current_test.actuals_folder = actuals_folder
				
				report_it ("datetime",
						   subfolder + tests + "\\" + test_name, test_url, test_type)

				test_in_selenium = getattr (mod, "test_in_selenium")
				result = test_in_selenium (current_test, function_to_call)

				report_it (bool (result))
		except:
			#test_repl may not be present
			traceback.print_exc (file=global_dict["debuglog"]) #test_store may not be present
			#global_dict["debuglog"].close()
			#global_dict["reslog"].close()
			#current_test.test_url = test_url #replace in the test_object
		
	global_dict["debuglog"].close()
	global_dict["reslog"].close()