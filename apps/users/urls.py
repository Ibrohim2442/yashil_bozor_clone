from django.urls import path

from . import views
from .views import CreateUserView, UserProfileCreateView, UserProfileDetailView, UserProfileUpdateView

urlpatterns = [
    path('user-create/', CreateUserView.as_view()),

    path('profiles/', UserProfileCreateView.as_view(), name='profile-create'),
    path('profiles/me/', UserProfileDetailView.as_view(), name='profile-detail'),
    path('profiles/me/update/', UserProfileUpdateView.as_view(), name='profile-update'),
]