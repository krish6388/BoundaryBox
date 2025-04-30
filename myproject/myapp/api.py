from ninja import NinjaAPI
from utils.database.connect_mongo import devDb
from pymongo import DESCENDING

api = NinjaAPI()

@api.get('/getMatchSchedule')
def get_match_schedule(request):
    print('Hello')
    data = devDb['match_schedule'].find_one({}, {'_id': 0})
    # del data['_id']
    print(data)
    return data

@api.get('/getFantasyMatchSchedule')
def get_fantasy_match_schedule(request):
    data = devDb['Fantasy_match_schedule'].find_one(
        filter={},
        projection={'_id': 0},
        sort=[('createdAt', DESCENDING)]
    )
    return data