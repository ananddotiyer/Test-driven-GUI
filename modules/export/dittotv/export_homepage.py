from export_misc import *
from ...libraries.verification import *

def WriteShowCarouselHome (f, rowCount, Show, current_test):
	try:
		expected = current_test.test_expected
		test_store = current_test.test_store
		test_params = current_test.test_params
		output_mode = current_test.output_mode

		if (output_mode == 'n'):
			return True
		
		if not VerifyFilter (Show, expected):
			return True

		f.write (Show["showtime"] + "\","),
		f.write ("\"" + Show["date"] + "\",")
		write_embed_replace_encode (f, Show["name"]),
		f.write ("\"" + Show["url"] + "\","),
		f.write ("\"" + Show["channel"] + "\"\n")

		#global_store (test_store, test_params, Show)
		return True
	except Exception, e:
		report_it ("Row " + str (rowCount + 1) + ":" + str(e) + " field is missing in the server response (JSON)\n")
		f.write ("\n")
		return False
	

def WriteSponsoredShowHome (f, rowCount, Show, current_test):
	try:
		expected = current_test.test_expected
		test_store = current_test.test_store
		test_params = current_test.test_params
		output_mode = current_test.output_mode

		if (output_mode == 'n'):
			return True
		
		if not VerifyFilter (Show, expected):
			return True

		
		write_embed_replace_encode (f, Show["name"]),
		f.write ("\"" + Show["url"] + "\","),
		f.write ("\"" + Show["time"] + "\"\n")

		#global_store (test_store, test_params, Show)
		return True
	except Exception, e:
		report_it ("Row " + str (rowCount + 1) + ":" + str(e) + " field is missing in the server response (JSON)\n")
		f.write ("\n")
		return False


def WriteShowCarouselHomeHeader (f, output_mode):
    if (output_mode != 'w'):
        return
    f.write ("Time" + ","),
    f.write ("Date" + ","),
    f.write ("Showname" + ","),
    f.write ("URL" + ","),
    f.write ("Channelname" + "\n")

def WriteSponsoredShowHomeHeader (f, output_mode):
    if (output_mode != 'w'):
        return
    f.write ("Showname" + ","),
    f.write ("URL" + ","),
    f.write ("ImageTransitionTime" + "\n")


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