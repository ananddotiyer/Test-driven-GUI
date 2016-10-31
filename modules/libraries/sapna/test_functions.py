#!/usr/bin/env python
from ...export.sapna.export_search import *
from ...export.sapna.export_products import *
from ...export.sapna.export_misc import *
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
def search(current_test):
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

    if expected["specific"] == "author":
        rowCount = 0

        author = GetAuthors(current_test)
        (name, url) = GetNames_Urls (current_test)
        crumbs = GetCrumbs(current_test)
        
        book = {} #dictionary to hold details of each book
        books = [] #list to hold all book dictionaries
       
        book['crumbs'] = crumbs
        for i in range (len (name)):
            book['name'] = name[i]
            book['author'] = author[i]
            book['url'] = url[i]
            books.append (book.copy())
        
        WriteAuthorSearchHeader (f, output_mode)
        for book in books:
            rowCount += 1
            result = WriteAuthorSearch (f, rowCount, book, current_test)
            result = result and VerifyExpected (book, expected)

    if expected["specific"] == "specs":
        rowCount = 0

        publisher = GetPublishers(current_test)
        (name, url) = GetNames_Urls (current_test)
        price = GetPrices(current_test, 'actual-price')
        
        book = {} #dictionary to hold details of each book
        books = [] #list to hold all book dictionaries

        for i in range (len (name)):
            book['name'] = name[i]
            book['publisher'] = publisher[i]
            book['url'] = url[i]
            book['price'] = price[i]
            books.append (book.copy())

        WriteSpecsSearchHeader (f, output_mode)
        for book in books:
            rowCount += 1
            result = WriteSpecsSearch (f, rowCount, book, current_test)
            result = result and VerifyExpected (book, expected)

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

################################################product##############################################################
def product_page(current_test):
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

    if expected["specific"] == "specs":
        product = {}
        product['title'] = GetTitle (current_test)[0]
        product['price'] = GetPrices(current_test, 'final-price')[0]
        
        rowCount = 1
        WriteProductSpecsHeader (f, output_mode)
        result = WriteProductSpecs (f, rowCount, product, current_test)
        result = result and VerifyExpected (product, expected)

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

#sapnaonline.com
def GetAuthors (current_test):
    data_dict = current_test.data

    #pattern_author = re.compile ("<div class=\"row product-book-author\">\n\t{8}<a href=\"//sapnaonline.com.*\">(.+)</a>")
    #author = re.findall(pattern_author, data_dict) #find author for each book

    xpath_author = "//div[@class='large-12 twelve small-12 tablet-8 columns product-book-author']/a"
    author = []
    for each in driver.find_elements_by_xpath (xpath_author):
        author.append (each.text)
    return author

def GetPrices (current_test, tagname):
    data_dict = current_test.data
    
    pattern_price = re.compile ("<span class=\"" + tagname + "\"><span class=\"ruppee\">`</span>(.*)</span>")
    price = re.findall(pattern_price, data_dict) #find price for each book

    #xpath_price = "//span[@class='actual-price']"
    #for some reason, identifying price elements using xpath isn't working, so use regex instead.
    #price = []
    #for each in driver.find_elements_by_xpath (xpath_price):
    #    price.append (each.text)
    return price

def GetNames_Urls (current_test):
    data_dict = current_test.data
    #pattern_books = re.compile ("<div class=\"row product-book-name\">\n\t{7}<a href=\"//(sapnaonline.com.*)\">(.+)</a>")
    #name_url = re.findall(pattern_books, data_dict) #find books, and urls

    xpath_book = "//div[@class='large-12 twelve small-12 tablet-8 columns product-book-name']/a"
    name = []
    url = []
    for each in driver.find_elements_by_xpath (xpath_book):
        name.append (each.text)
        url.append (each.get_attribute ("href"))
    return (name, url)

def GetPublishers (current_test):
    data_dict = current_test.data
    #pattern_publisher = re.compile ("<li><span class=\"details-spec\">Publisher:</span>(.*)</li>")
    #publisher = re.findall(pattern_publisher, data_dict) #find publisher for each book

    xpath_publisher = "//li/span[@class='details-spec'][contains(text(),'Publisher')]/.."
    publisher = []
    for each in driver.find_elements_by_xpath (xpath_publisher):
        publisher.append (each.text)
    return publisher

def GetTitle (current_test):
    data_dict = current_test.data
    #pattern_title = re.compile ("id=\"product-main-title\">\n\t{5}<a>(.+)</a>")
    #title = re.findall(pattern_title, data_dict) #find title for each book

    xpath_title = "//h1[@id='product-main-title']/a"
    title = []
    for each in driver.find_elements_by_xpath (xpath_title):
        title.append (each.text)
    return title

def GetCrumbs (current_test):
    data_dict = current_test.data

    xpath_crumbs = "//ul[@class='breadcrumbs']/li"
    crumbs = []
    for each in driver.find_elements_by_xpath (xpath_crumbs):
        crumbs.append (each.find_element_by_xpath ("./a").text)
    return crumbs