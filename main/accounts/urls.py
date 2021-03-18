from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('register', Register.as_view(), name='register'),
    path('activate/<slug:uidb64>/<slug:token>', activate, name='activate'),
    path('detail/<pk>', UserEditView.as_view(), name='user_detail'),
    # path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]