from concurrent.futures import ProcessPoolExecutor
from utils.modules.selenium_modules import *
from utils.modules.base_modules import *
from utils.selenium.chrome_driver import *
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from utils.helper.helper import find_element, find_elements, click_element, scroll_page_down
import http.client
from apscheduler.schedulers.background import BackgroundScheduler
from utils.helper.scrape_loop import scrape_in_loop
from utils.database.connect_mongo import *


def date_convertor(s):

    try:
        original_date_str = s

        original_format = '%a, %d %b %Y %I:%M %p'

        desired_format = '%Y-%m-%d %H:%M:%S'

        date_obj = datetime.datetime.strptime(original_date_str, original_format)
        
        formatted_date_str = date_obj.strftime(desired_format)

        return formatted_date_str
    except Exception as e:
        return ''


def schedule_matches(scheduler, json_data):
    for link in json_data:
        if json_data[link] == '':
            continue
        base_link = link.replace('/live', '').replace('/scorecard', '').replace('/info', '')
        scheduler.add_job(
            func=scrape_in_loop,
            trigger=DateTrigger(run_date=json_data[link]),
            args=[base_link, 10],
            id=base_link,
            replace_existing=True  
        )
    return scheduler

def scrape_fixtures(url, scheduler=None):
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(4)

    # SCROLL PAGE DOWN
    scroll_page_down(driver)
    d = {}
    json_data = {}
    
    while True:
        print('Next Btn Clicked')
        time.sleep(1)
        
        a = 1
        
        while True:
            print(a)
            try:
                date = find_element(driver, By.XPATH, f'//div[@class="date-wise-matches-card"]/div[{a}]/div/div')
                link_elm_lst = driver.find_elements(By.XPATH, f'//div[@class="date-wise-matches-card"]/div[{a}]/div[2]/div/app-fixture-match-card/ul/li/a')
                link_lst = [i.get_attribute('href') for i in link_elm_lst]
                time_lst = find_elements(driver, By.XPATH, f'//div[@class="date-wise-matches-card"]/div[{a}]/div[2]/div/app-fixture-match-card/ul/li/a[1]/div/div[2]/div')
                a+=1
                
                new_time_lst = [date_convertor(date + " " + item) for item in time_lst]
                json_data.update(dict(zip(link_lst, new_time_lst)))
                if date not in d:

                    d[date] = {
                        'time': time_lst,
                        'link': link_lst
                    }
                else:
                    d[date]['time'].extend(time_lst)
                    d[date]['link'].extend(link_lst)
            except Exception as e:
                break
        # print(d)
        try:
            date_lst = find_elements(driver, By.XPATH, '//div[@class="date"]/div[1]')
        except Exception as e: 
            break
        if len(date_lst) < 1:
            break

        # CLICK NEXT BTN
        try:
            click_element(driver, By.XPATH, '//div[@class="flex-center pagination"]/button[2]')
        except Exception as e:
            print('Error in clicking next btn')
            driver.get_screenshot_as_file('ss.jpg')
    
    driver.close()
    driver.quit()
    matchScheduleCol.insert_one(d)

    if scheduler == None:
        scheduler = BackgroundScheduler(executor=ProcessPoolExecutor())

    scheduler = schedule_matches(scheduler, json_data)
    
    # GET ALL SCHEDULED MATCHES
    all_jobs = scheduler.get_jobs()
    triggers = {}
    for job in all_jobs:
        print(f"Job ID: {job.id}, Trigger: {job.trigger}")
        triggers[job.id] = str(job.trigger)

    return triggers