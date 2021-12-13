from django.urls import path, re_path, include
from rest_framework import routers
from accounts import views

app_name = 'accounts'

router = routers.DefaultRouter()
router.register('register', views.RegisterViewSet)

urlpatterns = [
    path('api/login', views.LoginView.as_view(), name='login'),
    path('api/user', views.UserDetail.as_view(), name='user'),
    re_path('^api/', include(router.urls)),
    path('', include('uploads.urls'))
]
