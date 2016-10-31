#!/usr/bin/env python
from ...export.dittotv.export_channels import *
from ...export.dittotv.export_footer import *
from ...export.dittotv.export_homepage import *
from ...export.dittotv.export_tvshows import *
from ...export.dittotv.export_misc import *
from ..verification import *
from ...tests.tests_suite import *
from selenium import webdriver
import traceback

def test_in_selenium (current_test, function_to_call):

	try:
		result = False
		no_matches.clear()
		
		#open page in browser using selenium and get the server response
		global driver
		
		driver = webdriver.Firefox()
		driver.implicitly_wait(30)

		driver.get(current_test.test_url)
		
		current_test.data = driver.page_source

		#Parse the response, and verify the results
		result = function_to_call (current_test)
		
		driver.quit()
		
		return result
	except Exception: #so, you can continue with the next test
		traceback.print_exc (file=global_dict["debuglog"])

################################################search##############################################################
def homepage(current_test):
	filename = current_test.actuals_folder
	expected = current_test.test_expected
	data_dict = current_test.data
	output_mode = current_test.output_mode

	if not output_mode == 'n':
		f = open(filename + ".csv",output_mode)
	else:
		f = None
	
	rowCount = 0
	result = True

	if expected["specific"] == "showcarousel":
		rowCount = 0
		(showtime, date) = GetTime(current_test)
		(name, url, channel) = GetNames_Urls (current_test)
		#crumbs = GetCrumbs(current_test)
		
		show = {} #dictionary to hold details of each book
		shows = [] #list to hold all book dictionaries
		print name
		#show['crumbs'] = crumbs
		show['showtime'] = showtime
		show ['date'] = date
		for i in range (len (name)):
			show['name'] = name[i]
			show['url'] = url[i]
			show['channel'] = channel [i]
			shows.append (show.copy())
		
		WriteShowCarouselHomeHeader (f, output_mode)
		for show in shows:
			rowCount += 1
			result = WriteShowCarouselHome (f, rowCount, show, current_test)
			result = result and VerifyExpected (show, expected)

	if expected["specific"] == "sponsored":
		rowCount = 0

		(name, url, time) = GetSponsored(current_test)
		
		show = {} #dictionary to hold details of each book
		shows = [] #list to hold all book dictionaries
		
		for i in range (len (name)):
			show['name'] = name[i]
			show['url'] = url[i]
			show['time'] = time[i]
			shows.append (show.copy())
		
		WriteSponsoredShowHomeHeader (f, output_mode)
		for show in shows:
			rowCount += 1
			result = WriteSponsoredShowHome (f, rowCount, show, current_test)
			result = result and VerifyExpected (show, expected)
			
	if expected["specific"] == "term":
		rowCount = 0

		price = GetPrices(current_test,'actual-price')
		(name, url) = GetNames_Urls (current_test)
		
		book = {} #dictionary to hold details of each book
		books = [] #list to hold all book dictionaries

		for i in range (len (name)):
			book['name'] = name[i]
			book['url'] = url[i]
			book['price'] = price[i]
			books.append (book.copy())

		WriteProductSearchHeader (f, output_mode)
		for book in books:
			rowCount += 1
			result = WriteProductSearch (f, rowCount, book, current_test)
			result = result and VerifyExpected (book, expected)

	for no_match in no_matches.keys():
		if no_matches[no_match] > 0:
			print_string = "Expected " + expected[no_match] + " in " + no_match + ", but not found " + str (no_matches[no_match]) + "/" + str (rowCount) + " times!"
		else:
			print_string = "Expected " + expected[no_match] + " in " + no_match + ", and found in all " + str (rowCount) + " rows!"
			
		print (print_string)
		global_dict["debuglog"].write (print_string)
			
	result = result and VerifyRowCount (rowCount, expected["rowcount"])
			
	try:
		f.close()
	except:
		pass

	return result

################################################Livetv##############################################################
def livetv_page(current_test):
	filename = current_test.actuals_folder
	expected = current_test.test_expected
	data_dict = current_test.data
	output_mode = current_test.output_mode

	if not output_mode == 'n':
		f = open(filename + ".csv",output_mode)
	else:
		f = None
	
	rowCount = 0
	result = True
##################Recommended####################
	if expected["specific"] == "recommended":
		rowCount = 0
		(title,url) = GetTitles_Urls (current_test)
		
		program = {}
		programs = []
		
		i=0
		for i in range (len (title)):
			program['title'] = title[i]
			program['url'] = url[i]
			programs.append (program.copy())
			i+1
			
		WriteRecommendedHeader (f, output_mode)
		for program in programs:
			rowCount += 1
			result = WriteRecommended (f, rowCount, program, current_test)
			#print program
			result = result and VerifyExpected (program, expected)

##################Popular####################
	if expected["specific"] == "popular":
		rowCount = 0
		(title,url) = GetPopularTitles_Urls (current_test)
		
		program = {}
		programs = []
		
		i=0
		for i in range (len (title)):
			program['title'] = title[i]
			program['url'] = url[i]
			programs.append (program.copy())
			i+1
			
		WritePopularHeader (f, output_mode)
		for program in programs:
			rowCount += 1
			result = WritePopular (f, rowCount, program, current_test)
			#print program
			result = result and VerifyExpected (program, expected)


###All channels
	if expected["specific"] == "all":
		rowCount = 0
		title = GetChannelTitle (current_test)
		
		channel = {}
		channels = []
		
		print len(title)
		i=0
		for i in range (len (title)):
			channel['title'] = title[i]
			channels.append (channel.copy())
			i+1
		#print channels    
		WriteChannelAllHeader (f, output_mode)
		for channel in channels:
			rowCount += 1
			result = WriteChannelAll (f, rowCount, channel, current_test)
			result = result and VerifyExpected (channel, expected)

	for no_match in no_matches.keys():
		if no_matches[no_match] > 0:
			print_string = "Expected " + expected[no_match] + " in " + no_match + ", but not found " + str (no_matches[no_match]) + "/" + str (rowCount) + " times!"
		else:
			print_string = "Expected " + expected[no_match] + " in " + no_match + ", and found in all " + str (rowCount) + " rows!"
			
		print (print_string)
		global_dict["debuglog"].write (print_string)
			
	result = result and VerifyRowCount (rowCount, expected["rowcount"])
			
	try:
		f.close()
	except:
		pass

	return result

################################################Footer##############################################################
def Footer_Home(current_test):
	filename = current_test.actuals_folder
	expected = current_test.test_expected
	data_dict = current_test.data
	output_mode = current_test.output_mode

	if not output_mode == 'n':
		f = open(filename + ".csv",output_mode)
	else:
		f = None
	
	rowCount = 0
	result = True
##################Footer###################
	if expected["specific"] == "follow":
		rowCount = 0
		(title,url) = GetFooterFollowTitles_Urls (current_test)
		
		link = {}
		links = []
		
		i=0
		for i in range (len (title)):
			link['title'] = title[i]
			link['url'] = url[i]
			links.append (link.copy())
			i+1
			
		WriteFooterFollowHeader (f, output_mode)
		for link in links:
			rowCount += 1
			result = WriteFooterFollow (f, rowCount, link, current_test)
			#print program
			result = result and VerifyExpected (link, expected)

##################Footer top####################

	if expected["specific"] == "footertoplinks":
		rowCount = 0
		(title,url) = GetFooterTopTitles_Urls (current_test)
		#print title
		link = {}
		links = []
		
		i=0
		for i in range (len (title)):
			link['title'] = title[i]
			link['url'] = url[i]
			links.append (link.copy())
			i+1
			
		WriteFooterTopHeader (f, output_mode)
		for link in links:
			rowCount += 1
			result = WriteFooterTop (f, rowCount, link, current_test)
			#print program
			result = result and VerifyExpected (link, expected)
##################Footer Subscription##################
	
	if expected["specific"] == "footersubscription":
		rowCount = 0
		(button,url) = GetFooterSubscription_Urls (current_test)
		#print title
		plan = {}
		plans = []
		
		i=0
		for i in range (len (button)):
			plan['button'] = button[i]
			plan['url'] = url[i]
			plans.append (plan.copy())
			i+1
			
		WriteSubscriptionPlanHeader (f, output_mode)
		for plan in plans:
			rowCount += 1
			result = WriteSubscriptionPlan (f, rowCount, plan, current_test)
			#print program
			result = result and VerifyExpected (plan, expected)

	for no_match in no_matches.keys():
		if no_matches[no_match] > 0:
			print_string = "Expected " + expected[no_match] + " in " + no_match + ", but not found " + str (no_matches[no_match]) + "/" + str (rowCount) + " times!"
		else:
			print_string = "Expected " + expected[no_match] + " in " + no_match + ", and found in all " + str (rowCount) + " rows!"
			
		print (print_string)
		global_dict["debuglog"].write (print_string)
			
	result = result and VerifyRowCount (rowCount, expected["rowcount"])
			
	try:
		f.close()
	except:
		pass

	return result

################################################tvshows##############################################################
def tvshow_page(current_test):
	filename = current_test.actuals_folder
	expected = current_test.test_expected
	data_dict = current_test.data
	output_mode = current_test.output_mode

	if not output_mode == 'n':
		f = open(filename + ".csv",output_mode)
	else:
		f = None
	
	rowCount = 0
	result = True
	
	##################Recommended####################
	if expected["specific"] == "recommended":
		rowCount = 0
		(title,url) = GetTitlesTV_Urls (current_test)
		
		tvshow = {}
		programs = []
		
		i=0
		for i in range (len (title)):
			tvshow['title'] = title[i]
			tvshow['url'] = url[i]
			programs.append (tvshow.copy())
			
		WriteRecommendedTVShowHeader (f, output_mode)
		for tvshow in programs:
			rowCount += 1
			result = WriteRecommendedTVShow (f, rowCount, tvshow, current_test)
			result = result and VerifyExpected (tvshow, expected)

	for no_match in no_matches.keys():
		if no_matches[no_match] > 0:
			print_string = "Expected " + expected[no_match] + " in " + no_match + ", but not found " + str (no_matches[no_match]) + "/" + str (rowCount) + " times!"
		else:
			print_string = "Expected " + expected[no_match] + " in " + no_match + ", and found in all " + str (rowCount) + " rows!"
			
		print (print_string)
		global_dict["debuglog"].write (print_string)

	result = result and VerifyRowCount (rowCount, expected["rowcount"])

	try:
		f.close()
	except:
		pass

	return result

#Get Methods
def GetTime (current_test):
	data_dict = current_test.data

	xpath_time = "//div[@class='row livetv-carousel-container']//*[contains(@class,'livenow-info')]"
	showtime = ""
	hours = ""
	minutes = ""
	date = ""
	for each in driver.find_elements_by_xpath (xpath_time):
		now = (each.find_element_by_xpath (".//div[@class='live-tv-left']").text)
		hours = (each.find_element_by_xpath (".//div[@class='live-tv-left']/span").text)
		minutes = (each.find_element_by_xpath (".//div[@class='live-tv-right']/span").text)
		mer = (each.find_element_by_xpath (".//div[@class='live-tv-right']").text)
		showtime = now [:3] + " " +hours +":" +minutes+ " "+mer [:2]
		print showtime
		date = (each.find_element_by_xpath (".//span[@id='date']").text)
		print date    
	return (showtime, date)


def GetPrices (current_test, tagname):
	data_dict = current_test.data
	
	pattern_price = re.compile ("<span class=\"" + tagname + "\"><span class=\"ruppee\">`</span>(.*)</span>")
	price = re.findall(pattern_price, data_dict) #find price for each book
	return price

def GetNames_Urls (current_test):
	data_dict = current_test.data

	xpath_show = "//div[@id='show-carousel']//*[contains(@class,'owl-item')]"
	name = []
	url = []
	channel = []
	for each in driver.find_elements_by_xpath (xpath_show):
		name.append (each.find_element_by_xpath (".//div[@class='item']//b").text)
		url.append (each.find_element_by_xpath (".//a").get_attribute ("href"))
		channel.append (each.find_element_by_xpath (".//div[@class='show-name']/span").text)
	return (name, url, channel)

def GetSponsored (current_test):
	data_dict = current_test.data

	xpath_show = "//div[@id='sponcerd-show']//*[contains(@class,'owl-wrapper-outer')]"
	name = []
	url = []
	time = []
	for each in driver.find_elements_by_xpath (xpath_show):
		name.append (each.find_element_by_xpath (".//div[@class='item']").get_attribute ("title"))
		url.append (each.find_element_by_xpath (".//div[@class='item']").get_attribute ("href"))
		time.append (each.find_element_by_xpath (".//div[@class='owl-wrapper']").get_attribute ("style"))
	return (name, url, time)

def GetPublishers (current_test):
	data_dict = current_test.data

	xpath_publisher = "//li/span[@class='details-spec'][contains(text(),'Publisher')]/.."
	publisher = []
	for each in driver.find_elements_by_xpath (xpath_publisher):
		publisher.append (each.text)
	return publisher

def GetTitle (current_test):
	data_dict = current_test.data

	xpath_title = "//h1[@id='product-main-title']/a"
	title = []
	for each in driver.find_elements_by_xpath (xpath_title):
		title.append (each.text)
	return title

####Allchannels
def GetChannelTitle (current_test):
	data_dict = current_test.data

	xpath_channel = "//div[@class='subpattern2 movies-all-indi channels-all alltvchannel']/a"
	title = []
	for each in driver.find_elements_by_xpath (xpath_channel):
		title.append (each.get_attribute ("title"))
		
	return title

##Recommended
def GetTitles_Urls (current_test):
	data_dict = current_test.data
	
	xpath_program = "//div[@id='mrecommended']//*[contains(@class,'catalog-item')]/a"
	title = []
	url = []
	for each in driver.find_elements_by_xpath (xpath_program):
		title.append (each.get_attribute ("title"))
		url.append (each.get_attribute ("href"))
	return (title, url)

##Popular Livetv
def GetPopularTitles_Urls (current_test):
	data_dict = current_test.data
	
	xpath_program = "//div[@id='mpopular']//*[contains(@class,'catalog-item')]/a"
	title = []
	url = []
	for each in driver.find_elements_by_xpath (xpath_program):
		title.append (each.get_attribute ("title"))
		url.append (each.get_attribute ("href"))
	return (title, url)

def GetFooterFollowTitles_Urls (current_test):
	data_dict = current_test.data
	
	xpath_program = "//div[@class='footer']//*[contains(@class,'addthis_toolbox addthis_vertical')]/a"
	title = []
	url = []
	for each in driver.find_elements_by_xpath (xpath_program):
		title.append (each.get_attribute ("title"))
		url.append (each.get_attribute ("href"))
	return (title, url)

def GetFooterTopTitles_Urls (current_test):
	data_dict = current_test.data
	
	xpath_program = "//div[@class='row footer-top topmost-footer']//li/a"
	title = []
	url = []
	for each in driver.find_elements_by_xpath (xpath_program):
		title.append (each.text)
		url.append (each.get_attribute ("href"))
	return (title, url)

def GetFooterSubscription_Urls (current_test):
	data_dict = current_test.data
	
	xpath_program = "//div[@class='subscription footer-subscript']//*[contains(@class,'footer-btn')]//a"
	button = []
	url = []
	for each in driver.find_elements_by_xpath (xpath_program):
		button.append (each.text)
		url.append (each.get_attribute ("href"))
	return (button, url)

def GetCrumbs (current_test):
	data_dict = current_test.data

	xpath_crumbs = "//ul[@class='breadcrumbs']/li"
	crumbs = []
	for each in driver.find_elements_by_xpath (xpath_crumbs):
		crumbs.append (each.find_element_by_xpath ("./a").text)
	return crumbs

def GetTitlesTV_Urls (current_test):
	data_dict = current_test.data
	
	xpath_tvshow_recm = "//div[@id='mrecommended']//*[contains(@class,'catalog-item')]/a"
	title = []
	url = []
	for each in driver.find_elements_by_xpath (xpath_tvshow_recm):
		title.append (each.get_attribute ("title"))
		url.append (each.get_attribute ("href"))
	return (title, url)