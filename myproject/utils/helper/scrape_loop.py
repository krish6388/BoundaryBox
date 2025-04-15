from utils.modules.selenium_modules import *
from utils.modules.base_modules import *
from utils.selenium.chrome_driver import *
from scripts_data.cricex.live import scrape_live
from scripts_data.cricex.match_info import scrape_match_info
from scripts_data.cricex.scorecard import scrape_scorecard


def scrape_in_loop(url, time_gap):

    # SCRAPE MATCH-INFO ONE-TIME (IT WILL ALWAYS BE STATIC)
    match_info = scrape_match_info(url + '/info')

    # SCRAPE REAL-TIME DATA OF MATCH WITH GIVEN TIME-FREQUENCY(REFRESH RATE)
    while True:
        tres2 = scrape_scorecard(url + '/scorecard')

        # BREAK THE REFRESH LOOP IF RESULT IS NOT PENDING
        if tres2['result'] != "Pending":
            break
        tres1 = scrape_live(url + '/live')
        
        # TIME-GAP BTW REFRESH
        time.sleep(time_gap)
    return {
        'result': tres2['result']
    }
    