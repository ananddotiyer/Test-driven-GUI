from export_misc import *
from ...libraries.verification import *

def WriteFooterFollow (f, rowCount, Link, current_test):
	try:
		expected = current_test.test_expected
		test_store = current_test.test_store
		test_params = current_test.test_params
		output_mode = current_test.output_mode

		if (output_mode == 'n'):
			return True
		
		if not VerifyFilter (Link, expected):
			return True

		write_embed_replace_encode (f, Link["title"])
		f.write ("\"" + Link["url"] + "\"\n")

		#global_store (test_store, test_params, Link)
		return True
	except Exception, e:
		report_it ("Row " + str (rowCount + 1) + ":" + str(e) + " field is missing in the server response (JSON)\n")
		f.write ("\n")
		return False

def WriteFooterTop (f, rowCount, Link, current_test):
	try:
		expected = current_test.test_expected
		test_store = current_test.test_store
		test_params = current_test.test_params
		output_mode = current_test.output_mode

		if (output_mode == 'n'):
			return True
		
		if not VerifyFilter (Link, expected):
			return True

		write_embed_replace_encode (f, Link["title"])
		f.write ("\"" + Link["url"] + "\"\n")

		#global_store (test_store, test_params, Link)
		return True
	except Exception, e:
		report_it ("Row " + str (rowCount + 1) + ":" + str(e) + " field is missing in the server response (JSON)\n")
		f.write ("\n")
		return False

def WriteSubscriptionPlan (f, rowCount, Plan, current_test):
	try:
		expected = current_test.test_expected
		test_store = current_test.test_store
		test_params = current_test.test_params
		output_mode = current_test.output_mode

		if (output_mode == 'n'):
			return True
		
		if not VerifyFilter (Plan, expected):
			return True

		write_embed_replace_encode (f, Plan["button"])
		f.write ("\"" + Plan["url"] + "\"\n")

		#global_store (test_store, test_params, Plan)
		return True
	except Exception, e:
		report_it ("Row " + str (rowCount + 1) + ":" + str(e) + " field is missing in the server response (JSON)\n")
		f.write ("\n")
		return False

def WriteSubscriptionPlanHeader (f, output_mode):
    if (output_mode != 'w'):
        return
    f.write ("SubscribeButton" + ","),
    f.write ("URL" + "\n")


def WriteFooterFollowHeader (f, output_mode):
    if (output_mode != 'w'):
        return
    f.write ("SocialApp" + ","),
    f.write ("URL" + "\n")

def WriteFooterTopHeader (f, output_mode):
    if (output_mode != 'w'):
        return
    f.write ("FooterTopLinkTitles" + ","),
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