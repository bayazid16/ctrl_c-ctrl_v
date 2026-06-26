from django.urls import path
from .views import HealthAPIView, TickerAnalysisView   

urlpatterns = [
    path('analyze-ticket/', TickerAnalysisView.as_view(), name='ticker-analysis'),
    path('health/', HealthAPIView.as_view(), name='health-check'),
]