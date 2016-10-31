import json
import datetime
from modules.tests.tests_suite import *
import re

def VerifyFilter (actual, expected):
    retValue = True
    try:
        for each in expected["filter"]["location"].split ('\\'):
            actual = actual[each]
    except:
        pass #No location is specified.  So, filter from the base location.
    
    try:
        for each in expected["filter"]:
            global_dict["debuglog"].write ("Actual: " + str (actual[each]) + ", Expected: " + expected["filter"][each] + "\n")
            if (isinstance (actual[each], list)):
                if not (expected["filter"][each] in (actual[each])):
                    global_dict["debuglog"].write ("Values don't match\n")
                    retValue = False
                    break
            elif not (isinstance (actual[each], dict)):
                if not (str (actual[each]) == expected["filter"][each]):
                    retValue = False
                    break
    except:
        pass #filter dictionary might not be available in the test
    return retValue

def VerifyRowCount (actual_rowCount, exp_rowCount):
    if not (exp_rowCount == actual_rowCount):
        print (str (exp_rowCount) + " rows expected, but " + str (actual_rowCount) + "found!")
        global_dict["debuglog"].write (str (exp_rowCount) + " rows expected, but " + str (actual_rowCount) + "found!")
        return False
    else:
        print (str (exp_rowCount) + " rows expected, and " + str (exp_rowCount) + "found!")
        global_dict["debuglog"].write (str (exp_rowCount) + " rows expected, and " + str (exp_rowCount) + "found!")
        return True

def VerifyExpected (actual, expected):
    result = True
    actual_flattened = ""
    
    try:
        for exp in expected.keys():
            if (exp == "rowcount") or (exp == "specific") or (exp == "filter"):
                continue;
    
            if not no_matches.has_key (exp):
                no_matches[exp] = 0

            if (isinstance (actual[exp], list)):
                for list_item in actual[exp]:
                    actual_flattened += str (list_item) + ","
            else:
                actual_flattened = str (actual[exp])
                    
            if not (actual_flattened.lower().find(expected[exp].lower()) >= 0): #does not contain expected string
                no_matches[exp] += 1
                #print ("Expected " + expected[exp] + " in " + exp + ", but not found!")
                #global_dict["debuglog"].write ("Expected " + expected[exp] + " in " + exp + ", but not found!\n")
                result = False
    except:
        result = False

    return result

def report_start ():
    global_dict["reslog"].write ("test_path,test_url,test_type,executed_at,time_spent (sec),result\n")
    global_dict["start_time"] = datetime.datetime.now()
    
def report_it (result, test="", api_url="", api_type=""):
    #print (result)
    if isinstance (result, bool):
        if (result):
            print ("All is well!!")
            global_dict["debuglog"].write ("All is well!!\n")
            global_dict["reslog"].write ("PASS\n")
        else:
            global_dict["reslog"].write ("FAIL\n")
    else:
        result = str (result)
        global_dict["stop_time"] = datetime.datetime.now()
        date_time = global_dict["stop_time"].strftime('%Y-%m-%d %H:%M:%S')
        time_spent = str ((global_dict["stop_time"] - global_dict["start_time"]).total_seconds())
        result_string = test + " (Executed: " + date_time + ", " + time_spent + " seconds)"
        
        if result == "datetime":
            global_dict["debuglog"].write ("\n**" + result_string + "**\n") #only if this is the test header
            print ("**************************************************************************************")
            print (result_string)
            print ("**************************************************************************************")
            
            #Hyper-link the test to the appropriate output .csv.  For the right hyperlinking technique, refer to http://stackoverflow.com/questions/6563091/can-excel-interpret-the-urls-in-my-csv-as-hyperlinks
            test_title = test
            test = re.sub (r"^\\(.+)\\.*\\(.+)$", r"\1\\actuals\\\2", test) #lazy match ensures that only the test name is replaced.
            global_dict["reslog"].write ("\"=HYPERLINK(\"\"" + test + ".csv\"\"" + "," + "\"\"" + test_title + "\"\")\"" + "," +
                                         api_url + "," + api_type + "," + date_time + "," + time_spent + ",")
        else:
            global_dict["debuglog"].write (result)
            print (result)
            
