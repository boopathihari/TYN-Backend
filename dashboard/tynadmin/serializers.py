from rest_framework import serializers
from .models import Startup

class IndustryAcceptedInvitedCountSerializer(serializers.Serializer):
    industry = serializers.CharField()
    accepted_count = serializers.IntegerField()
    invited_count = serializers.IntegerField()

class StatusCountSerializer(serializers.Serializer):
    status = serializers.CharField()
    count = serializers.IntegerField()


class UserPersonaCountSerializer(serializers.Serializer):
    user_type = serializers.CharField()
    count = serializers.IntegerField()

class StartupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Startup
        fields = ['startup_id', 'name', 'category', 'query_count', 'poc_accepted', 'poc_delivered', 'is_verified']


class StartupCategorySerializer(serializers.Serializer):
    category = serializers.CharField()
    total_startups = serializers.IntegerField()
    verified_startups = serializers.IntegerField()