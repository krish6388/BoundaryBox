from utils.modules.selenium_modules import *
from utils.modules.base_modules import *
from utils.selenium.chrome_driver import *

# FIND TEXT-LIST OF ELEMENT-LIST
def find_elements(driver, by, xpath):
    try:
        lst = []
        elm_lst = driver.find_elements(by, xpath)
        lst+= [i.text for i in elm_lst]
        return lst
    except Exception as e:
        lst = []
        elm_lst = driver.find_elements(by, xpath)
        lst+= [i.text for i in elm_lst]
        return lst

# FIND TEXT OF SINGLE ELEMENT
def find_element(driver, by, xpath):
    return driver.find_element(by, xpath).text
    
# CLICK ELEMENT
def click_element(driver, by, xpath):
    a = driver.find_element(by, xpath)
    driver.execute_script("arguments[0].click();", a)
    return

# SCROLL PAGE DOWN TILL END
def scroll_page_down(driver):
    SCROLL_PAUSE_TIME = 2

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height