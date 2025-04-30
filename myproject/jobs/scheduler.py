from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from concurrent.futures import ProcessPoolExecutor

from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger
from scripts_data.cricex.fixtures import scrape_fixtures
from scripts_data.cricex.live import scrape_live
from utils.helper.scrape_loop import scrape_in_loop
from scripts_data.criclytics.upcoming_matches import scrape_upcoming_fantasy_matches
from scripts_data.criclytics.fantasy_team import get_fantasy_team

def schedule_job():
	print("Starting actual job")
	# print(get_fantasy_team('https://www.cricket.com/live-score/sunrisers-hyderabad-vs-mumbai-indians-match-41-indian-premier-league-2025-257255/criclytics'))
	# scrape_fixtures(url='https://crex.live/fixtures/match-list')
	# return
	daily_trigger = CronTrigger(
        year="*", month="*", day="*", hour="19", minute="52", second="00"
    )
	scheduler = BackgroundScheduler(executor=ProcessPoolExecutor())
	# scrape_fixtures('https://crex.live/fixtures/match-list', scheduler)
	
	scheduler.start()
	all_jobs = scheduler.get_jobs()

	for job in all_jobs:
		print(f"Job ID: {job.id}, Trigger: {job.trigger}")

	scheduler.add_job(
        func=scrape_fixtures,
        trigger=daily_trigger,
        # seconds=24*,
        args=['https://crex.live/fixtures/match-list', scheduler],
        id='Fixtures',
        replace_existing=True,
		misfire_grace_time=36000
    )
	print('End Job')