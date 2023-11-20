from django.urls import path

from .views import (
    BoardListCreateAPIView,
    BoardRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    path("boards/", BoardListCreateAPIView.as_view()),
    path("boards/<slug:slug>/", BoardRetrieveUpdateDestroyAPIView.as_view()),
]