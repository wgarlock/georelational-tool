from django.urls import path

from .views import StateAPIView, StateView

urlpatterns = [
    path('api/state', StateAPIView.as_view()),
    path('<int:pk>', StateView.as_view()),
]
