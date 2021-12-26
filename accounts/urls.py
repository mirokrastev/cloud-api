from django.urls import path, re_path, include
from rest_framework import routers
from accounts import views

app_name = 'accounts'

router = routers.DefaultRouter()
router.register('register', views.RegisterViewSet)

urlpatterns = [
    path('api/auth/login', views.LoginView.as_view(), name='login'),
    path('api/auth/logout', views.LogoutView.as_view(), name='logout'),
    path('api/user', views.UserDetail.as_view(), name='user'),
    re_path('^api/auth/', include(router.urls)),
]
