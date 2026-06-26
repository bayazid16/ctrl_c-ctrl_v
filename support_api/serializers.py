from rest_framework import serializers
from .models import TickerAnalysis

class TickerAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = TickerAnalysis
        fields = '__all__'