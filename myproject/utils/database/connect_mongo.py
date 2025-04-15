from utils.modules.base_modules import *
from dotenv import load_dotenv
import os
load_dotenv()

devClient = pymongo.MongoClient(os.environ.get('MONGODB_DEV_URI'))
devDb = devClient['Crex']
matchCommentaryCol = devDb['match_commentary']
matchScoreCardCol = devDb['match_scorecard']
matchInfoCol = devDb['match_info']
matchScheduleCol = devDb['match_schedule']