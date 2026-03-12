from django.urls import path

from . import views
from .views import CreateUserView, UserProfileCreateView, UserProfileDetailUpdateView, FavoriteListCreateView, \
    FavoriteDeleteView

urlpatterns = [
    path('', CreateUserView.as_view()),

    path('profiles/', UserProfileCreateView.as_view()),
    path('profiles/me/', UserProfileDetailUpdateView.as_view()),

    path('favorites', FavoriteListCreateView.as_view()),
    path('favorites/<int:pk>/', FavoriteDeleteView.as_view())
]