from django.db import models

class TickerAnalysis(models.Model):
    #user input 
    ticket_id = models.CharField(max_length=100, unique=False)
    complaint=models.TextField()
    transaction_history = models.JSONField(default=list)

    #ai output
    relevant_transaction_id = models.CharField(max_length=100, null=True, blank=True)
    evidence_verdict = models.CharField(max_length=50)
    case_type = models.CharField(max_length=100)
    severity = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    agent_summary = models.TextField()
    recommended_next_action = models.TextField()
    customer_reply = models.TextField()
    human_review_required = models.BooleanField(default=False)
    confidence = models.FloatField(null=True, blank=True )
    reason_codes = models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket ID: {self.ticket_id} - Case Type: {self.case_type}"



# Create your models here.
