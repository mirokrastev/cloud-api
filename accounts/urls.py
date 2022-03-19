from django.urls import path, re_path, include
from rest_framework import routers
from accounts import views

app_name = 'accounts'

auth_router = routers.DefaultRouter()
auth_router.register('register', views.RegisterViewSet)

router = routers.DefaultRouter()
router.register('user', views.UserViewSet, basename='user')

urlpatterns = [
    path('api/auth/login/', views.LoginView.as_view(), name='login'),
    path('api/auth/logout/', views.LogoutView.as_view(), name='logout'),
    re_path('^api/auth/', include(auth_router.urls)),
    re_path('^api/', include(router.urls)),
]
