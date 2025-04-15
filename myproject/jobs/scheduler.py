from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from concurrent.futures import ProcessPoolExecutor

from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger
from scripts_data.cricex.fixtures import scrape_fixtures
from scripts_data.cricex.live import scrape_live
from utils.helper.scrape_loop import scrape_in_loop
def schedule_job():
	print("Starting actual job")
	# scrape_fixtures(url='https://crex.live/fixtures/match-list')
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