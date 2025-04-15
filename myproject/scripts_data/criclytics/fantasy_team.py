from utils.modules.selenium_modules import *
from utils.modules.base_modules import *
from utils.selenium.chrome_driver import *
from utils.helper.helper import find_element, find_elements, click_element, scroll_page_down


def make_perf_dict(squad_name_lst, squad_perf_lst):
    perf_dict = {}
    for i in range(len(squad_name_lst)):
        perf_dict[squad_name_lst[i]] = squad_perf_lst[i]
    return perf_dict

def get_fantasy_team(url):
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(3)

    squadA__name_lst = find_elements(driver, By.XPATH, '//p[@class="text-sm font-medium text-black dark:text-white pb-1"]')
    squadA_perf_lst = find_elements(driver, By.XPATH, '//div[@class="flex items-center text-gray-2"]/p[1]')
    squadA_perf_dict = make_perf_dict(squadA__name_lst, squadA_perf_lst)

    click_element(driver, By.XPATH, '')

    squadB__name_lst = find_elements(driver, By.XPATH, '//p[@class="text-sm font-medium text-black dark:text-white pb-1"]')
    squadB_perf_lst = find_elements(driver, By.XPATH, '//div[@class="flex items-center text-gray-2"]/p[1]')
    squadB_perf_dict = make_perf_dict(squadA__name_lst, squadA_perf_lst)

    return {
        'teamA': squadA_perf_dict,
        'teamB': squadB_perf_dict
    }