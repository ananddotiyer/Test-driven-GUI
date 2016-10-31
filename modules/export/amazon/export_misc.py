from ...libraries.verification import *

def write_none(f, val):
	if val is None:
		f.write (","),
	else:
		if isinstance (val, int):
			f.write (str (val) + ","),
		else:
			f.write (val + ",")
	

def write (f, column, embed=False, ends_with=','):
    if column is None:
        f.write (","),
    else:
        if isinstance (column, list):
            all_each = ""
            for each in column:
                all_each += each + ";"
            column = all_each #concatenate everything into a string
        elif isinstance  (column, int):
            column = str (column)

        #if '\"' in column:
        #    embed = True

        embed = True        
        if embed:
            f.write ("\"")

        f.write (column.replace ("\"", "'").replace (",", "+").encode('utf-8')),

        if embed:
            f.write ("\"")

        f.write (ends_with)

def write_thumbnails(f, thumbnails):
	thumbnail_string = ""
	for thumbnail in thumbnails:
		try:
			thumbnail_string += thumbnail + ":" + thumbnails[thumbnail]['url'] + ";"
		except:
			pass
	write (f, thumbnail_string)

def write_fill (f, count, max):
	while count < max:
		f.write (","),
		count += 1
	
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