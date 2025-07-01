from rest_framework import serializers
from .models import AnalyticsEvent, ABTest, ABTestParticipant, PerformanceMetric, ErrorLog

class AnalyticsEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticsEvent
        fields = '__all__'
        read_only_fields = ['id', 'timestamp']

class ABTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ABTest
        fields = '__all__'

class ABTestParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ABTestParticipant
        fields = '__all__'

class PerformanceMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceMetric
        fields = '__all__'
        read_only_fields = ['timestamp']

class ErrorLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorLog
        fields = '__all__'
        read_only_fields = ['id', 'timestamp']
