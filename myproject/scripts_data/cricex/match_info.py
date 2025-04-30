from utils.modules.selenium_modules import *
from utils.modules.base_modules import *
from utils.selenium.chrome_driver import *
from utils.helper.helper import find_element, find_elements
from utils.database.connect_mongo import matchInfoCol

def update_match_info_in_db(match_url, obj):
    # SOFT DELETE PREVIOUS INFO
    result = matchInfoCol.update_one(
        {'matchUrl': match_url}, 
        {'$set': {'status': 1, 'updatedAt': datetime.datetime.now()}}  
    )

    # INSERT LATEST INFO
    matchInfoCol.insert_one(obj)

    # PERMANENTLY DELETE OLD INFO
    result = matchInfoCol.delete_one(
        {
            'matchUrl': match_url,
            'status': 1
        }
    )


def scrape_match_info(url):
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(4)

    match_name = find_element(driver, By.XPATH, '//h1[@class="name-wrapper"]/span')
    try:
        toss_info = find_element(driver, By.XPATH, '//div[@class="toss-wrap"]/p')
    except:
        toss_info = 'N/A'
    schedule_info = find_element(driver, By.XPATH, '//div[@class="match-date"]/div')
    # loc_info = find_element(driver, By.XPATH, '//div[@class="match-date match-venue"]/div') 
    
    try:
        teams_lst = find_elements(driver, By.XPATH, '//div[@class="form-team-name"]')
        team_name = {
            'team1': teams_lst[0],
            'team2': teams_lst[1]
        }
    except:
        team_name = {}
    
    try:
        head_to_head_lst = find_elements(driver, By.XPATH, '//div[@class="team-wins"]/div'),
        head_to_head = {
            'team1': head_to_head_lst[0][0],
            'team2': head_to_head_lst[0][2]
        }
    except:
        head_to_head = {}

    try:
        weather_conditions = {
            'temp': find_element(driver, By.XPATH, '//div[@class="weather-temp"]'),
            'sky': find_element(driver, By.XPATH, '//div[@class="weather-cloudy-text"]'),
            'humidity': find_element(driver, By.XPATH, '//div[@class="align-center weather-place-hum-text humidity-text"]/div'),
            'rain': find_element(driver, By.XPATH, '//div[@class="align-center weather-place-hum-text"]/div'),
        }
    except:
        weather_conditions = {}

    try:
        ump_lst = find_elements(driver, By.XPATH, '//div[@class="umpire-val"]')
        ump_info = {
            'On-field': ump_lst[0],
            'Third': ump_lst[1],
            'Referee': ump_lst[2]
        }
    except:
        ump_info = {}
    
    try:
        ball_type_lst = find_elements(driver, By.XPATH, '//div[@class="flex align-center w100"]/div')
        ball_type = {
            'Pace': ball_type_lst[0],
            'Spin': ball_type_lst[1]
        }
    except:
        ball_type = {}
    avg_scr_lst = find_elements(driver, By.XPATH, '//span[@class="venue-avg-val"]')
    leg_scr_lst = find_elements(driver, By.XPATH, '//span[@class="venue-score"]')
    try:
        venue_stats = {
        'totalMatch': find_element(driver, By.XPATH, '//div[@class="match-count"]'),
        'winOrder': {
            'batFirst': find_element(driver, By.XPATH, '//div[@class="venue-text-padding"]/div[1]/span[2]'),
            'bowlFirst': find_element(driver, By.XPATH, '//div[@class="venue-text-padding"]/div[2]/span[2]')
        },
        'scoreDetails': {
            'avgScore': {
                'firstInn': avg_scr_lst[0],
                'secondInn': avg_scr_lst[1]
            },
            'legendScore': {
                'highest': {
                    'total': leg_scr_lst[0],
                    'chased': leg_scr_lst[2]
                },
                'lowest': {
                    'total': leg_scr_lst[1],
                    'defended': leg_scr_lst[3]
                }
            }
        }
        
    }

    except :
        venue_stats = {}

    try:
        team_comparison = {
            'matchPlayed': {
                'team1': find_element(driver, By.XPATH, '//table[@class="table table-borderless colHeader"]/tbody/tr[1]/td[1]'),
                'team2': find_element(driver, By.XPATH, '//table[@class="table table-borderless colHeader"]/tbody/tr[1]/td[3]')
            },
            'win': {
                'team1': find_element(driver, By.XPATH, '//table[@class="table table-borderless colHeader"]/tbody/tr[2]/td[1]'),
                'team2': find_element(driver, By.XPATH, '//table[@class="table table-borderless colHeader"]/tbody/tr[2]/td[3]')
            },
            'scoreDetails': {
                'avgScore': {
                    'team1': find_element(driver, By.XPATH, '//table[@class="table table-borderless colHeader"]/tbody/tr[3]/td[1]'),
                    'team2': find_element(driver, By.XPATH, '//table[@class="table table-borderless colHeader"]/tbody/tr[3]/td[3]')
                },
                'highestScore': {
                    'team1': find_element(driver, By.XPATH, '//table[@class="table table-borderless colHeader"]/tbody/tr[4]/td[1]'),
                    'team2': find_element(driver, By.XPATH, '//table[@class="table table-borderless colHeader"]/tbody/tr[4]/td[3]')
                },
                'lowestScore': {
                    'team1': find_element(driver, By.XPATH, '//table[@class="table table-borderless colHeader"]/tbody/tr[5]/td[1]'),
                    'team2': find_element(driver, By.XPATH, '//table[@class="table table-borderless colHeader"]/tbody/tr[5]/td[3]')
                },
            }
            
        }
    except: 
        team_comparison = {}
    try:
        result = find_element(driver, By.XPATH, '//span[@class="font3 font4"]')
    except:
        result = 'Pending'

    data = {
        'matchName': match_name,
        'teamName': team_name,
        'schedule': schedule_info,
        # 'location': loc_info,
        'toss': toss_info,
        'headToHead': head_to_head,
        'wetherCondition': weather_conditions,
        'Umpire': ump_info,
        'prefBall': ball_type,
        'venueStats': venue_stats,
        'teamComparison': team_comparison,
        'matchUrl': url,
        'status': 0,
        'result': result,
        'updatedAt': datetime.datetime.now()
        }
    
    update_match_info_in_db(url, data)

    del data['_id']
    driver.close()
    driver.quit()
    
    return data
