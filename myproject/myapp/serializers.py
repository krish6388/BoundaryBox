from rest_framework import serializers

# SERIALIZER TO START ONE-TIME SCRAPING OF ANY MATCH/FIXTURE
class LiveMatchSerializer(serializers.Serializer):
    STATUS_CHOICES = [
        ('live', 'Live'),
        ('match info', 'Match info'),
        ('scorecard', 'Scorecard'),
        ('fixtures', 'Fixtures'),
    ]
    liveMatchUrl = serializers.CharField()
    type = serializers.ChoiceField(choices=STATUS_CHOICES)

# SERIALIZER TO START REAL-TIME SCRAPING OF A LIVE MATCH
class RealTimeSerializer(serializers.Serializer):
    base_url = serializers.CharField()
    time_gap = serializers.IntegerField()

class UpcomingFantasyMatchSerializer(serializers.Serializer):
    url = serializers.CharField()

class FantasyTeamSerializer(serializers.Serializer):
    url = serializers.CharField()