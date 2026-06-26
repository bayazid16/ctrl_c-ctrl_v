from rest_framework import serializers
from .models import TickerAnalysis

class TickerAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = TickerAnalysis
        fields = '__all__'

        read_only_fields = (
            "relevant_transaction_id",
            "evidence_verdict",
            "case_type",
            "severity",
            "department",
            "agent_summary",
            "recommended_next_action",
            "customer_reply",
            "human_review_required",
            "confidence",
            "reason_codes",
            "created_at",
        )