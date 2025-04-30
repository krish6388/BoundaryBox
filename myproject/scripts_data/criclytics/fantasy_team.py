from utils.modules.selenium_modules import *
from utils.modules.base_modules import *
from utils.selenium.chrome_driver import *
from utils.helper.helper import find_element, find_elements, click_element, scroll_page_down
from utils.database.connect_mongo import devDb


def make_perf_dict(squad_name_lst, squad_perf_lst):
    perf_dict = {}
    for i in range(len(squad_name_lst)):
        perf_dict[squad_name_lst[i]] = squad_perf_lst[i]
    return perf_dict

def get_fantasy_team(url):
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(3)

    sentiment_to_number = {
        'VERY BAD': 1.0,
        'BAD': 2.0,
        'NEUTRAL': 3.0,
        'GOOD': 4.0,         # Optional if 'GOOD' is not in the list
        'VERY GOOD': 5.0,
        'NOT AVAILABLE': 0.0
    }

    player_name_elm_lst = driver.find_elements(By.XPATH, '//div[@class="flex items-center justify-between border-b px-2 py-2"]/div/div/div/div/a')
    player_name_lst = []
    for i in player_name_elm_lst:
        player_name_lst.append(i.get_attribute('title'))
        print(i.get_attribute('title'))
    
    ranking_lst_raw = find_elements(driver, By.XPATH, '//div[@class="flex items-center justify-between border-b px-2 py-2"]/div[4]/div/p')
    ranking_lst = [sentiment_to_number[s] for s in ranking_lst_raw]
    
    # for i in range(len(ranking_lst)):
    #     print(f'{player_name_lst[i]}: {ranking_lst[i].strip()}')

    # rank_obj1 = rank_obj2 = {}
    # for i in range(player_name_lst[:11]):
    #     rank_obj1 = {
    #         'player': player_name_lst[i],
    #         'rank': ranking_lst[i]
    #     }
    # for i in range(player_name_lst[11:]):
    #     rank_obj2 = {
    #         'player': player_name_lst[i],
    #         'rank': ranking_lst[i]
    #     }

    team_name_lst = find_elements(driver, By.XPATH, '//h3[@class="ml-2 text-sm font-bold text-text-header hover:underline"]')
    print(team_name_lst)

    obj = {
        'team1': team_name_lst[0].strip(),
        'ranking_team1': {
            'player_lst': player_name_lst[:11],
            'rank_lst': ranking_lst[:11]
        },
        'team2': team_name_lst[-1].strip(),
        'ranking_team2': {
            'player_lst': player_name_lst[11:],
            'rank_lst': ranking_lst[11:]
        },
        'link': driver.current_url,
        'created_at': datetime.datetime.now()
    }
    print(obj)
    devDb['ranking_datas'].update_many(
        {"link": obj["link"]},
        {"$set": obj}
    )
    print(obj)
    return obj
    # squadA__name_lst = find_elements(driver, By.XPATH, '//p[@class="text-sm font-medium text-black dark:text-white pb-1"]')
    # squadA_perf_lst = find_elements(driver, By.XPATH, '//div[@class="flex items-center text-gray-2"]/p[1]')
    # squadA_perf_dict = make_perf_dict(squadA__name_lst, squadA_perf_lst)
    # print(squadA_perf_dict)

    # click_element(driver, By.XPATH, '')

    # squadB__name_lst = find_elements(driver, By.XPATH, '//p[@class="text-sm font-medium text-black dark:text-white pb-1"]')
    # squadB_perf_lst = find_elements(driver, By.XPATH, '//div[@class="flex items-center text-gray-2"]/p[1]')
    # squadB_perf_dict = make_perf_dict(squadA__name_lst, squadA_perf_lst)

    # return {
    #     'teamA': squadA_perf_dict,
    #     'teamB': squadB_perf_dict
    # }