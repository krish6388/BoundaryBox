from utils.modules.selenium_modules import *
from utils.modules.base_modules import *
from utils.selenium.chrome_driver import *
from utils.helper.helper import find_element, find_elements, click_element
from utils.database.connect_mongo import matchScoreCardCol
from bson import json_util


def update_scorecard_in_db(match_url, obj):
    # SOFT DELETE PREVIOUS SCORECARD
    result = matchScoreCardCol.update_one(
        {'matchUrl': match_url}, 
        {'$set': {'status': 1, 'updatedAt': datetime.datetime.now()}}  
    )

    # INSERT LATEST SCORECARD
    matchScoreCardCol.insert_one(obj)

    # PERMANENTLY DELETE OLD SCORECARD
    result = matchScoreCardCol.delete_one(
        {
            'matchUrl': match_url,
            'status': 1
        }
    )

def scrape_data(driver):
    batsmen_lst = find_elements(driver, By.XPATH, '//div[@class="batsman-name"]/a/span')
    batsmen_lst = [x for x in batsmen_lst if x != 'IMPACT']
    decision_lst = find_elements(driver, By.XPATH, '//div[@class="decision"]')
    bowler_lst = find_elements(driver, By.XPATH, '//div[@class="bowler-name"]/a/span')
    score_elm_lst = driver.find_elements(By.XPATH, '//td[@class="rowColFirst"]/div')
    bowler_lst = bowler_lst[:-len(batsmen_lst) + decision_lst.count('NOT OUT')]
    # print(bowler_lst)
    score_lst = []
    for i in score_elm_lst:
        try:
            score_lst.append(str(float(i.text)))
        except:
            pass
    # print(score_lst)
    bat_sublists = [score_lst[i:i + 5] for i in range(0, len(batsmen_lst) * 5, 5)] #len(score_lst[:len(batsmen_lst)*5]), 5)]
    ball_sublists = [score_lst[len(batsmen_lst)*5 + i:len(batsmen_lst)*5 + i + 5] for i in range(0, (len(bowler_lst)) * 5, 5)] #len(score_lst[len(batsmen_lst)*5:]), 5)]
    # print(bat_sublists)
    # print(ball_sublists)
    batsmen_header = ["R", "B", "4s", "6s", "SR"]
    bat_json = {}
    print(batsmen_lst, len(batsmen_lst))
    print(decision_lst, len(decision_lst))
    for i, x in enumerate(batsmen_lst):
        bat_json[x] = dict(zip(batsmen_header, bat_sublists[i]))
        bat_json[x]["Status"] = decision_lst[i]
    bowler_header = ["B", "M", "R", "W", "ER"]
    ball_json = {}
    for i, x in enumerate(bowler_lst):
        ball_json[x] = dict(zip(bowler_header, ball_sublists[i]))
    
    scorecard = {
        "Batting": bat_json,
        "Bowling": ball_json
    }
    return scorecard
        

def scrape_scorecard(url):
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(4)

    try:
        result = find_element(driver, By.XPATH, '//span[@class="font3 font4"]')
    except Exception as e:
        result = 'Pending'
    
    team_name_lst = find_elements(driver, By.XPATH, '//span[@class="team-name"]')
    run_over_lst = find_elements(driver, By.XPATH, '//div[@class="score-over"]/span')
    final_scorecard = {}
    json_data = scrape_data(driver)
    final_scorecard[find_element(driver, By.XPATH, '//div[@class="team-tab m-right bgColor"]/div/div/span')] = json_data
    
    try:
        click_element(driver, By.XPATH, '//div[@class="team-tab m-right"]')
        time.sleep(1)
        json_data = scrape_data(driver)
        final_scorecard[find_element(driver, By.XPATH, '//div[@class="team-tab m-right bgColor"]/div/div/span')] = json_data
    except Exception as e:
        print(e)
        pass

    driver.close()
    driver.quit()

    final_scorecard['matchUrl'] = url
    final_scorecard['result'] = result
    final_scorecard['status'] = 0
    final_scorecard['updatedAt'] = datetime.datetime.now()

    update_scorecard_in_db(url, final_scorecard)

    del final_scorecard['_id']
    print(final_scorecard)

    return final_scorecard