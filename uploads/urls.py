from django.urls import path
from uploads import views

urlpatterns = [
    path('api/stats', views.StatsView.as_view(), name='stats'),
]
