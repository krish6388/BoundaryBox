# import sys
# sys.path.insert(0, 'E:\ORUphones\TestSetupConfig\myproject')
from utils.modules.selenium_modules import *

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.149 Safari/537.36"

options = webdriver.ChromeOptions()

options.add_argument("--headless=new")

options.add_argument(f'user-agent={user_agent}')
    
options.add_argument("--window-size=1920,1080")

options.add_argument('--ignore-certificate-errors')

options.add_argument('--allow-running-insecure-content')

options.add_argument("--disable-extensions")

options.add_argument("--disable-notifications")

options.add_argument("--proxy-server='direct://'")

options.add_argument("--proxy-bypass-list=*")

options.add_argument("--start-maximized")

options.add_argument('--disable-gpu')

options.add_argument('--disable-dev-shm-usage')

options.add_argument('--no-sandbox')

options.add_argument('--ignore-ssl-errors')

options.add_argument("--disable-redirects")

options.add_argument("--disable-javascript")


