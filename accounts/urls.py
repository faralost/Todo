from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.views import RegisterView, UserDetailView, UsersListView, UserChangeView, UserPasswordChangeView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', RegisterView.as_view(), name="registration"),
    path('<slug:slug>/', UserDetailView.as_view(), name='detail_profile'),
    path('', UsersListView.as_view(), name='users'),
    path('<slug:slug>/change/', UserChangeView.as_view(), name='profile_change'),
    path('<slug:slug>/password_change', UserPasswordChangeView.as_view(), name='password_change')
]
