from export_misc import *
from ...libraries.verification import *

def WriteAuthorSearch (f, rowCount, Book, current_test):
	try:
		expected = current_test.test_expected
		test_store = current_test.test_store
		test_params = current_test.test_params
		output_mode = current_test.output_mode

		if (output_mode == 'n'):
			return True
		
		if not VerifyFilter (Book, expected):
			return True

		write_embed_replace_encode (f, Book["name"])
		f.write ("\"" + Book["author"] + "\","),
		
		crumb_string = ""
		for crumb in Book["crumbs"]:
			crumb_string += crumb + "/"
		
		f.write ("\"" + crumb_string + "\",")
		f.write ("\"" + Book["url"] + "\"\n")

		#global_store (test_store, test_params, Book)
		return True
	except Exception, e:
		report_it ("Row " + str (rowCount + 1) + ":" + str(e) + " field is missing in the server response (JSON)\n")
		f.write ("\n")
		return False

def WriteSpecsSearch (f, rowCount, Book, current_test):
	try:
		expected = current_test.test_expected
		test_store = current_test.test_store
		test_params = current_test.test_params
		output_mode = current_test.output_mode

		if (output_mode == 'n'):
			return True
		
		if not VerifyFilter (Book, expected):
			return True

		write_embed_replace_encode (f, Book["name"])
		f.write ("\"" + Book["publisher"] + "\","),
		f.write ("\"" + Book["price"] + "\","),
		f.write ("\"" + Book["url"] + "\"\n")

		#global_store (test_store, test_params, Book)
		return True
	except Exception, e:
		report_it ("Row " + str (rowCount + 1) + ":" + str(e) + " field is missing in the server response (JSON)\n")
		f.write ("\n")
		return False

def WriteProductSearch (f, rowCount, Book, current_test):
	try:
		expected = current_test.test_expected
		test_store = current_test.test_store
		test_params = current_test.test_params
		output_mode = current_test.output_mode

		if (output_mode == 'n'):
			return True
		
		if not VerifyFilter (Book, expected):
			return True

		write_embed_replace_encode (f, Book["name"])
		f.write ("\"" + Book["price"] + "\","),
		f.write ("\"" + Book["url"] + "\"\n")

		#global_store (test_store, test_params, Book)
		return True
	except Exception, e:
		report_it ("Row " + str (rowCount + 1) + ":" + str(e) + " field is missing in the server response (JSON)\n")
		f.write ("\n")
		return False

def WriteAuthorSearchHeader (f, output_mode):
    if (output_mode != 'w'):
        return
    f.write ("Book name" + ","),
    f.write ("Author" + ","),
    f.write ("Breadcrumbs" + ","),
    f.write ("URL" + "\n")

def WriteSpecsSearchHeader (f, output_mode):
    if (output_mode != 'w'):
        return
    f.write ("Book name" + ","),
    f.write ("Publisher" + ","),
    f.write ("Price" + ","),
    f.write ("URL" + "\n")

def WriteProductSearchHeader (f, output_mode):
    if (output_mode != 'w'):
        return
    f.write ("Product name" + ","),
    f.write ("Price" + ","),
    f.write ("URL" + "\n")

def write_embed_replace_encode (f, column):
    if column is None:
        f.write (","),
    else:
        f.write ("\"" + column.replace ("\"", "'").encode('utf') + "\","),

def global_store (api_store, api_params, data):
    #storing into global_dict
    try:
        for each in api_store["response"]:
            try:
                global_dict[each] = data[api_store["response"][each]]
                print (global_dict[each])
            except:
                print ("Unable to find " + each + " in the server response!  None stored.")

        for each in api_store["request"]:
            try:
                global_dict[each] = api_params[api_store["request"][each]]
                print (global_dict[each])
            except:
                print ("Unable to find " + each + " in the request parameters!  None stored.")

    except:
        pass