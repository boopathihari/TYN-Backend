# urls.py
from django.urls import path
from .views import IndustryAcceptedInvitedCountView,StatusCountView,UserPersonaCountView,SessionCountAPI,AverageResponseTimeView,StartupCategoryStatsAPIView,TotalConversionRateView

urlpatterns = [
    path('api/industriesCount/', IndustryAcceptedInvitedCountView.as_view(), name='industry_accepted_invited_count'),
    path('api/status-count/', StatusCountView.as_view(), name='status_count'),
    path('api/user-persona-count/', UserPersonaCountView.as_view(), name='user_persona_count'),
    path('api/session-count/', SessionCountAPI.as_view(), name='session-count-api'),
    path('api/average-response-time/', AverageResponseTimeView.as_view(), name='average-response-time'),
    path('api/startup-category/', StartupCategoryStatsAPIView.as_view(), name='startup_category_stats'),
    path('api/ConversionRate/', TotalConversionRateView.as_view(), name='startup_funnel_data'),
]
