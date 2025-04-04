from django.contrib.auth.views import LogoutView
from django.urls import path

from users.services import UserService
from users.views import RegisterView, CustomLoginView, CustomUserUpdate, CustomPasswordResetView, \
    CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView, CustomUserDetailView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('confirm/<str:token>/', UserService.email_verification, name='confirm'),
    path('user/update/<int:pk>/', CustomUserUpdate.as_view(), name='user_update'),
    path('user/profile/<int:pk>/', CustomUserDetailView.as_view(), name='user_profile'),

    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(),name='password_reset_complete'),
]
