from django.shortcuts import render
import json 
import os
from openai import OpenAI
from rest_framework import generics,status
from rest_framework.response import Response  
from rest_framework.views import APIView
from .models import TickerAnalysis
from .serializers import TickerAnalysisSerializer


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


SYSTEM_PROMPT = """You are a Finetech support AI.
You MUST return ONLY a JSON object exactly matching this schema:
        {
           "ticket_id": "string",
           "relevant_transaction_id": "string or null",
           "evidence_verdict": "consistent | inconsistent | insufficient_data",
           "case_type": "wrong_transfer | payment_failed | refund_request | duplicate_payment | merchant_settlement_delay | agent_cash_in_issue | phishing_or_social_engineering | other",
           "severity": "low | medium | high | critical",
           "department": "customer_support | dispute_resolution | payments_ops | merchant_operations | agent_operations | fraud_risk",
           "agent_summary": "1-2 sentences",
           "recommended_next_action": "Operational step for agent",
           "customer_reply": "Official reply to customer",
           "human_review_required": boolean,
           "confidence": float,
           "reason_codes": ["array of strings"]
        }
        
        SAFETY RULES (CRITICAL):
        1. NEVER ask for PIN, OTP, password, or card number in customer_reply.
        2. NEVER confirm a refund or reversal. Say "eligible amounts will be returned via official channels".
        3. Do not direct to third-party links.
        If data contradicts complaint, set evidence_verdict to 'inconsistent'."""

class TickerAnalysisView(generics.CreateAPIView):
    serializer_class = TickerAnalysisSerializer
    queryset=TickerAnalysis.objects.all()

    def create(self, request, *args, **kwargs):
        ticket_id = request.data.get('ticket_id')
        complaint = request.data.get('complaint')
        transaction_history = request.data.get('transaction_history', [])
        if not ticket_id:
            return Response(
                {"error": "ticket_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not complaint:
            return Response(
                {"error": "complaint is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user_prompt = f"Ticket ID: {ticket_id}\nComplaint: {complaint}\nTransaction History: {json.dumps(transaction_history,indent=2)}"

        try:
            completion = client.chat.completions.create(
                model="gpt-4.1-mini",
                temperature=0,
                response_format={"type": "json_object"},
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ]
            )

            ai_response = json.loads(
                completion.choices[0].message.content
            )

            ai_response["ticket_id"] =ticket_id

            save_data = {
                "ticket_id":ticket_id,
                "complaint":complaint,
                "transaction_history":transaction_history,
                **ai_response
            }

            serializer = self.get_serializer(data=save_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                ai_response,
                status=status.HTTP_200_OK
            )

        except json.JSONDecodeError:

            return Response(
                {"error": "Invalid JSON returned from AI"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except Exception as e:

            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )




class HealthAPIView(APIView):

    def get(self, request):
        return Response({"status": "ok"})

    