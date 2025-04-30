from django.shortcuts import render,HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LiveMatchSerializer, RealTimeSerializer, UpcomingFantasyMatchSerializer, FantasyTeamSerializer
from scripts_data.cricex.live import scrape_live
from scripts_data.cricex.match_info import scrape_match_info
from scripts_data.cricex.fixtures import scrape_fixtures
from scripts_data.cricex.scorecard import scrape_scorecard
from scripts_data.criclytics.upcoming_matches import scrape_upcoming_fantasy_matches
from scripts_data.criclytics.fantasy_team import get_fantasy_team
from utils.helper.scrape_loop import scrape_in_loop


# VIEW TO START ONE-TIME SCRAPING OF ANY MATCH/FIXTURE
class liveMatchSerializer(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LiveMatchSerializer(data=request.data)
        if serializer.is_valid():
            # Process the valid data
            data = serializer.validated_data
            url = data.get('liveMatchUrl')
            type = data.get('type')

            if type == 'live':
                data2 = scrape_live(url)

            elif type == 'match info':
                data2 = scrape_match_info(url+'/info')

            elif type == 'fixtures':
                data2 = scrape_fixtures(url)

            elif type == 'scorecard':
                data2 = scrape_scorecard(url + '/scorecard')

            return Response({"message": type, "Data Scraped": data2}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# VIEW TO START REAL-TIME SCRAPING OF A LIVE MATCH
class realTimeSerializer(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RealTimeSerializer(data=request.data)
        if serializer.is_valid():
            # Process the valid data
            data = serializer.validated_data
            base_url = data.get('base_url')
            time_gap = data.get('time_gap')

            # Processing logic here
            base_url = base_url.replace('/live', '').replace('/scorecard', '').replace('/info', '')
            data2 = scrape_in_loop(base_url, time_gap)
            return Response({"message": type, "Data Scraped": data2}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class upcomingFantasyMatchSerializer(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UpcomingFantasyMatchSerializer(data=request.data)
        if serializer.is_valid():
            # Process the valid data
            data = serializer.validated_data
            url = data.get('url')
            json_data = scrape_upcoming_fantasy_matches(url)
            return Response({"message": 'Schedule', "DataScraped": json_data}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class fantasyTeamSerializer(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FantasyTeamSerializer(data=request.data)
        if serializer.is_valid():
            # Process the valid data
            data = serializer.validated_data
            url = data.get('url')
            json_data = get_fantasy_team(url)
            return Response({"message": 'FantasyTeam', "DataScraped": json_data}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)