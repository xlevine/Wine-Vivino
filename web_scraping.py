import re
import time
import math
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
import pandas as pd

#color_list = ['red','white','sparkling','rose']
#color_list = ['sparkling','rose','red','white']
#color_list = ['red','white']
A = np.arange(0,30,1); B = np.arange(30,50,5); C = np.arange(50,250,10); D = np.arange(250,550,50)
list_target_price = np.concatenate((A,B,C,D))
time_out = 4

def set_page_option(driver,color,country):

    #1. select country of shipping 
    xpath_root='//*[@id="navigation-container"]/div[2]/nav/div[2]/div[1]/div/div'
    if country=='FR':
        # shipping in FR
        xpath='//*[@id="navigation-container"]/div[2]/nav/div[2]/div[1]/div[2]/div[1]/ul/li[8]/a'
    elif country=='ES':
        # shipping in SP
        xpath='//*[@id="navigation-container"]/div[2]/nav/div[2]/div[1]/div[2]/div[1]/ul/li[7]/a'
    elif country=='IT':
        # shipping in IT
        xpath='//*[@id="navigation-container"]/div[2]/nav/div[2]/div[1]/div[2]/div[1]/ul/li[12]/a'
    shipping_root_element = driver.find_elements_by_xpath(xpath_root)[0]
    shipping_root_element.click()    
    shipping_opt_element = driver.find_elements_by_xpath(xpath)[0]
    shipping_opt_element.click()

    time.sleep(time_out)
    #2. select color
    if color=='red':
    # red
        xpath='//*[@id="explore-page-app"]/div/div/div[2]/div[1]/div/div[1]/div[2]/label[1]'
    elif color=='white':
    # white
        xpath='//*[@id="explore-page-app"]/div/div/div[2]/div[1]/div/div[1]/div[2]/label[2]'
    elif color=='sparkling':
    # sparkling
        xpath='//*[@id="explore-page-app"]/div/div/div[2]/div[1]/div/div[1]/div[2]/label[3]'
    elif color=='rose':
    # rose
        xpath='//*[@id="explore-page-app"]/div/div/div[2]/div[1]/div/div[1]/div[2]/label[4]'
    elif color=='dessert':
    # dessert
        xpath='//*[@id="explore-page-app"]/div/div/div[2]/div[1]/div/div[1]/div[2]/label[5]'
    elif color=='port':
    # port
        xpath='//*[@id="explore-page-app"]/div/div/div[2]/div[1]/div/div[1]/div[2]/label[6]'
    color_element = driver.find_elements_by_xpath(xpath)[0]
    color_element.click()        

    time.sleep(time_out)
    #3. select no rating class
    xpath='//*[@id="explore-page-app"]/div/div/div[2]/div[1]/div/div[3]/label[5]/div[1]'
    rating_element = driver.find_elements_by_xpath(xpath)[0]
    rating_element.click()

    time.sleep(time_out)
#    # select language
#    xpath_root='//*[@id="navigation-container"]/div[2]/nav/div[2]/div[2]/div'
#    xpath='//*[@id="navigation-container"]/div[2]/nav/div[2]/div[2]/div[2]/div[1]/ul/li[4]/a'
#    language_root_element = driver.find_elements_by_xpath(xpath_root)[0]
#    language_root_element.click()
#    language_opt_element = driver.find_elements_by_xpath(xpath)[0]
#    language_opt_element.click()

def execute_slider_move(driver,side,target):

    [price_left, price_right] = read_price(driver)
    if side=='right':
        price_ini = price_right
        xpath_slider = '//*[@id="explore-page-app"]/div/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div[5]'
    elif side=='left':
        price_ini = price_left
        xpath_slider = '//*[@id="explore-page-app"]/div/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div[4]'

    time.sleep(time_out)
    price = price_ini
    increment = 0
    while price!=target:
        time.sleep(time_out)    
        slider = driver.find_element_by_xpath(xpath_slider)
        webdriver.ActionChains(driver).click_and_hold(slider).move_by_offset(increment, 0).release().perform()
        [price_left, price_right] = read_price(driver)        

        if side=='right':
            price_new = price_right
        elif side=='left':
            price_new = price_left

        if (np.sign(price_new-target)!=np.sign(price-target)):
            increment = 0
        elif ((target<price) and (price==price_new)):
            increment = increment - 1 
        elif ((target>price) and (price==price_new)):
            increment = increment + 1 

        price = price_new

def move_slider(driver,target_min,target_max):

    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    driver.execute_script("window.scroll(0, 0);")
    [price_min, price_max] = read_price(driver)
    while ((price_min!=target_min) or (price_max!=target_max)):
        execute_slider_move(driver,'right',target_max)
        execute_slider_move(driver,'left',target_min)                    
        time.sleep(time_out)
        [price_min, price_max] = read_price(driver)

def read_price(driver):

    xpath_price_min='//*[@id="explore-page-app"]/div/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div[1]'
    xpath_price_max='//*[@id="explore-page-app"]/div/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div[2]'
    price_min_element = driver.find_element_by_xpath(xpath_price_min)
    price_max_element = driver.find_element_by_xpath(xpath_price_max)
    price_min_text = price_min_element.text
    price_max_text = price_max_element.text
    price_min = int(''.join(filter(str.isdigit,price_min_text)))
    price_max = int(''.join(filter(str.isdigit,price_max_text)))

    return price_min, price_max

def scroll(driver, timeout, cutoff):

    Num_scroll=0

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    T=0
    ntry=5
    while True:

        new_height = exectute_scroll(driver,timeout)
        if new_height == last_height:
            scheight = .1
            while scheight < 9.9:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % scheight)
                scheight += .1
            print('failed loading page at ' + str(Num_scroll) + " scroll-downs")
            # If heights are the same it will try N more times to scroll down
            T=T+1 
            if T==ntry:
           # If heights are the same after N attempts, exit
                print("Scrolling has reached bottom of page at " + str(Num_scroll) + " scroll-downs")
                break            
        else:
            T = 0
            Num_scroll = Num_scroll + 1

        last_height = new_height
        element_num = Num_scroll*25

        print('completed ' + str(Num_scroll) + ' scroll-downs' )
        print('displaying ' + str(Num_scroll*25)+' elements')

        if element_num >=1.001*cutoff:
            print("Scrolling has exceeded total number of items at " + str(Num_scroll) + " scroll-downs")
            break

def exectute_scroll(driver,scroll_pause_time):

        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        return new_height

def find_number(driver):

    time.sleep(time_out)
    xpath_num='//*[@id="explore-page-app"]/div/div/h2'
    num_element = driver.find_elements_by_xpath(xpath_num)[0]
    number_str = num_element.text

    [First, Second] = number_str.split('entre')
    number = int(''.join(filter(str.isdigit,First)))
    
    return number

def import_all(country):
    
    for color in color_list:
        print(color)
        main(country,color)

def main(country='FR',color='red',start_price=0,end_price=500):

    url_path = 'https://www.vivino.com/explore'
    browser_type = 'firefox'
#    browser_type = 'chrome'

    driver = open_browser(browser_type,url_path)
    driver.implicitly_wait(time_out)
    driver.get(url_path)    

    set_page_option(driver,color,country)

    if ((start_price==0) and (end_price==500)):
        Vintage = pd.DataFrame(columns = ['Country','Region','Domain','Cru','Year','ratings','reviews','link','Price'])
    else:
        Vintage = pd.read_pickle('vintage' + '_'+ color + '_'+  country + '.pkl')

    item_number = find_number(driver)
    nprice = len(list_target_price)
#    delta_price = np.minimum(np.maximum(math.ceil((300*nprice)/item_number),2),6)
    delta_price = 2
    nstart = np.argwhere(list_target_price==start_price)
    nend   = np.argwhere(list_target_price==end_price)
    index_price = np.arange(nstart,nend+1,delta_price)
    for n in index_price:
        try: 
            target_min = list_target_price[n]
            if (n+delta_price)<nprice:
                target_max = list_target_price[n+delta_price]
            else:    
                target_max = np.amax(list_target_price)
            print('Items in range of ' + str(target_min) + ' to '+ str(target_max) + ' euro')

            move_slider(driver,target_min,target_max)

            wine_cutoff = find_number(driver)            
            print('there are ' + str(wine_cutoff) + ' items')
            last_height = 0

            #  wine_cutoff = 25
            if wine_cutoff>25:
                print('start scrolling')
                scroll(driver, time_out, wine_cutoff)
                print('end of scrolling')
            else:
                print('no scrolling')

            for item_id in np.arange(1,wine_cutoff+1,1):
                print("reading item " + str(item_id) + " out of " + str(wine_cutoff))
                try:
                    [Country, Region, Domain, Cru, Year, ratings, reviews, link, Price] = execute_search(driver,item_id)
                    Vintage.loc[len(Vintage)] = [Country, Region, Domain, Cru, Year, ratings, reviews, link, Price]
                except:
                    print("no data found in item " + str(item_id))
            print(Vintage)                    
            Vintage.to_pickle('vintage' + '_'+ color + '_'+  country + '.pkl')    
        except: 
            print("no data found in price range")
            
    print('Success: end of iteration in ' + color + ' category sold in ' + country)
    print(Vintage)                    
    close_browser(driver)

def open_browser(type,url_path):

    if 'chrome' in type:
        # open Chrome
        option = webdriver.ChromeOptions()    
        chrome_prefs = {}
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
        option.experimental_options["prefs"] = chrome_prefs
        option.add_argument("--incognito")
        driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=option)
    elif 'firefox'in type:
        # open Firefox
        option = webdriver.FirefoxProfile()
        option.set_preference('permissions.default.image', 2)
        option.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
        option.set_preference("browser.privatebrowsing.autostart", True)
        driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver',firefox_profile=option)

    return driver

def close_browser(driver):

    driver.close()

def diagnose_end_list(driver,item_id):

    root_item ='//*[@id="explore-page-app"]/div/div/div[2]/div[2]/div[1]/'
    numb_item ='div[' + str(item_id)+ ']'
    xpath_url='/div[2]/div[1]/a'
    url_element = driver.find_elements_by_xpath(root_item + numb_item + xpath_url)[0]
        
def execute_search(driver,item_id):

    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

    root_item ='//*[@id="explore-page-app"]/div/div/div[2]/div[2]/div[1]/'
    numb_item ='div[' + str(item_id)+ ']'

    # Region
    xpath_reg='/div[2]/div[1]/div/a[3]'
    reg_element = driver.find_elements_by_xpath(root_item + numb_item + xpath_reg)[0]
    Region = reg_element.text    
    # Domain, Cru and Link
    xpath_url='/div[2]/div[1]/a'
    url_element = driver.find_elements_by_xpath(root_item + numb_item + xpath_url)[0]
    vintage = url_element.text   
    [Domain, Cru_full] = vintage.split('\n')
    Cru = ''.join([i for i in Cru_full if not i.isdigit()])
    if 'N.V.' in Cru:
        Year = 'N.V'
    else:
        Year = int(''.join(filter(str.isdigit,Cru_full))) 
    link = url_element.get_attribute("href")
    # Ratings
    xpath_ratings='/div[2]/div[2]/div/div/div[1]'
    ratings_element = driver.find_elements_by_xpath(root_item + numb_item + xpath_ratings)[0]
    ratings = ratings_element.text
    # Reviews
    xpath_reviews='/div[2]/div[2]/div/div/div[2]/div[2]'
    reviews_element = driver.find_elements_by_xpath(root_item + numb_item + xpath_reviews)[0]
    reviews_str = reviews_element.text
    reviews = int(''.join(filter(str.isdigit,reviews_str)))
    # Price
    xpath_price='/div[2]/div[2]/button/span'
    xpath_price_opt='/div[2]/div[2]/button'
    price_opt_element = driver.find_elements_by_xpath(root_item + numb_item + xpath_price_opt)[0]
    price_opt_str = price_opt_element.text
    if 'Ver' in price_opt_str:
        price_opt_element.click()
        xpath_price ='//*[@id="baseModal"]/div/div/div[2]/div[2]/div[3]/a'            
        pause_time=0.3
        time.sleep(pause_time)
        try: 
            price_element = driver.find_elements_by_xpath(xpath_price)[0]            
            price_str = price_element.text
            if '.' in price_str:
                [int_str, dec_str] = price_str.split('.')
                Price_int = int(''.join(filter(str.isdigit,int_str)))        
                Price_dec = int(''.join(filter(str.isdigit,dec_str)))        
                Price = Price_int + Price_dec*0.01
            else:
                Price = int(''.join(filter(str.isdigit,price_str)))
        except:
            Price = 'N.A.'                            

        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

    else:
        try:
            price_element = driver.find_elements_by_xpath(root_item + numb_item + xpath_price)[0]
            price_str = price_element.text

            if '.' in price_str:
                [int_str, dec_str] = price_str.split('.')
                Price_int = int(''.join(filter(str.isdigit,int_str)))        
                Price_dec = int(''.join(filter(str.isdigit,dec_str)))        
                Price = Price_int + Price_dec*0.01
            else:
                Price = int(''.join(filter(str.isdigit,price_str)))                    
        except:
            Price = 'N.A.'

    print(Price)

    # Country
    xpath_country='/div[2]/div[1]/div/a[2]'
    country_element = driver.find_elements_by_xpath(root_item + numb_item + xpath_country)[0]
    Country = country_element.text

    return Country, Region, Domain, Cru, Year, ratings, reviews, link, Price

#    find_element_by_tag_name
#    find_element_by_class_name
#    find_element_by_css_selector 

#def onfly_scroll(driver, timeout, last_height=0):

#    scroll_pause_time = timeout

    # Get scroll height
#    last_height = driver.execute_script("return document.body.scrollHeight")

#    new_height = execute_scroll(driver,scroll_pause_time)

#    return new_height

#    onfly_scroll='False'
#        if onfly_scroll=='True':
#            try:
#                diagnose_end_list(driver,item_id)
#            except:            
#                new_height = onfly_scroll(driver,time_out,last_height)
#                if new_height == last_height:
#                    # If heights are the same it will exit the function
#                    print("EOF at " + str(item_id))
#                    break
#                last_height = new_height
