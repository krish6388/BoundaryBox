from utils.modules.selenium_modules import *
from utils.modules.base_modules import *
from utils.selenium.chrome_driver import *
from utils.helper.helper import find_element, find_elements, click_element, scroll_page_down

def scrape_upcoming_fantasy_matches(url):
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(3)

    upcom_fant_match_lst = find_elements(driver, By.XPATH, '//p[@class="md:block hidden cursor-pointer hover:underline max-w-[250px]"]/a')
    upcom_fant_match_lst = list(set(upcom_fant_match_lst))

    match_num_loc_lst = find_elements(driver, By.XPATH, '//div[@class="flex flex-row items-center font-mnr text-xs text-gray-12 font-medium"]/p')
    match_num_loc_lst = list(set(match_num_loc_lst))
    match_num_lst = []
    match_loc_lst = []
    flag = 0
    for i in match_num_loc_lst:
        if flag == 0:
            match_num_lst.append(i)
            flag = 1
        else:
            match_loc_lst.append(i)
            flag = 0
    
    match_date_lst = find_elements(driver, By.XPATH, '//p[@class="mb-2.5 mt-0.5"]')
    match_date_lst = list(set(match_date_lst))

    match_time_lst = find_elements(driver, By.XPATH, '//p[@class="h-5"]')
    match_time_lst = list(set(match_time_lst))

    match_rival_lst = find_elements(driver, By.XPATH, '//p[@class=" text-xs min-w-[25%] text-gray-13 dark:text-white font-medium"]')
    match_rival_lst = list(set(match_rival_lst))

    match_link_elm_lst = driver.find_elements(By.XPATH, '//a[@class="hidden md:block bg-white border overflow-hidden dark:bg-gray dark:border-none rounded-lg w-full p-2"]')
    match_link_lst = []
    for link_elm in match_link_elm_lst:
        match_link_lst.append(link_elm.get_attribute('href'))

    # CREATE OBJ
    rival_count = 0
    obj_lst = []
    for i in len(match_link_lst):
        obj = {
            'matchName': upcom_fant_match_lst[i],
            'matchNum': match_num_lst[i],
            'matchLoc': match_loc_lst[i],
            'teamA': match_rival_lst[rival_count],
            'teamB': match_rival_lst[rival_count + 1],
            'matchDate': match_date_lst[i],
            'matchTime': match_time_lst[i],
            'createdAt': datetime.datetime.now()
        }
        rival_count += 2
        obj_lst.append(obj)

    return obj_lst
    

    