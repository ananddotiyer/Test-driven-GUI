#!/usr/bin/env python
from ...export.amazon.export_search import *
from ...export.amazon.export_misc import *
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

################################################amazon_search##############################################################
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

    if expected["specific"] == "specs":
        rowCount = 0

        title = GetTitles(current_test)
        price = GetPrices (current_test)
        
        product = {} #dictionary to hold details of each product
        products = [] #list to hold all product dicts

        for i in range (len (title)):
            product['title'] = title[i]
            product['price'] = price[i]
            products.append (product.copy())

        WriteSpecsSearchHeader (f, output_mode)
        for product in products:
            rowCount += 1
            result = WriteSpecsSearch (f, rowCount, product, current_test)
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
def GetPrices (current_test):
    data_dict = current_test.data
    
    xpath_price = "//span[@class='a-size-base a-color-price s-price a-text-bold']"
    price = []
    for each in driver.find_elements_by_xpath (xpath_price):
        price.append (each.text)
    return price

def GetTitles (current_test):
    data_dict = current_test.data

    xpath_title = "//h2[@class='a-size-medium a-color-null s-inline s-access-title a-text-normal']"
    title = []
    for each in driver.find_elements_by_xpath (xpath_title):
        title.append (each.text)
    return title