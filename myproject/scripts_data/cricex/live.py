from utils.modules.selenium_modules import *
from utils.modules.base_modules import *
from utils.selenium.chrome_driver import *
from utils.helper.helper import find_element, find_elements, click_element, scroll_page_down
from utils.database.connect_mongo import matchCommentaryCol

def update_commentary_in_db(match_url, obj_lst):
    # SOFT DELETE PREVIOUS COMMENTARY
    result = matchCommentaryCol.update_many(
        {'matchUrl': match_url}, 
        {'$set': {'status': 1, 'updatedAt': datetime.datetime.now()}}  
    )

    # INSERT LATEST COMMENTARY
    matchCommentaryCol.insert_many(list(obj_lst))

    # PERMANENTLY DELETE OLD COMMENTARY
    result = matchCommentaryCol.delete_many(
        {
            'matchUrl': match_url,
            'status': 1
        }
    )

def scrape_live(match_url):
    driver = webdriver.Chrome(options=options)
    driver.get(match_url)
    time.sleep(6)
    # scroll_page_down(driver)
    print('Scroll Completed')
    result = 'Pending'
    try:
        result = find_element(driver, By.XPATH, '//span[@class="font3 font4"]')
    except:
        pass

    try:
        cmt_lst = find_elements(driver, By.XPATH, '//span[@class="cm-b-comment-c1"]')
        print(cmt_lst)
    except:
        cmt_lst = ['N/A']

    try:
        action_lst = find_elements(driver, By.XPATH, '//div[@class="d-flex text-align-start comm-update-space"]/span')
    except:
        action_lst = ['N/A']

    try:
        over_lst = find_elements(driver, By.XPATH, '//span[@class="cm-b-over"]')
    except:
        over_lst = ['N/A']
    
    driver.close()
    driver.quit()

    if len(over_lst) == 0:
        over_lst = ['N/A']
    if len(cmt_lst) == 0:
        cmt_lst = ['N/A']
    if len(action_lst) == 0:
        action_lst = ['N/A']
    action_lst = list(map(lambda x: '0' if x == '' else x, action_lst))

    if len(action_lst) == 2*len(over_lst):
        for i in range(1, len(action_lst), 2):
            cmt_lst[i//2] += ":" + action_lst[i]
        action_lst = [action_lst[i] for i in range(0, len(action_lst), 2)]
    mx_len = max(len(over_lst), len(action_lst), len(cmt_lst))
    over_lst += ['N/A']*(mx_len - len(over_lst))
    action_lst += ['N/A']*(mx_len - len(action_lst))
    cmt_lst += ['N/A']*(mx_len - len(cmt_lst))
    
    data = {
        'overs': over_lst,
        'action': action_lst,
        'comment': cmt_lst,
    }

    df = pd.DataFrame(data)
    df['matchUrl'] = match_url
    df['status'] = 0
    df['updatedAt'] = datetime.datetime.now()
    
    obj_lst = df.to_dict(orient='records')

    update_commentary_in_db(match_url, obj_lst)

    print(data)
    return data