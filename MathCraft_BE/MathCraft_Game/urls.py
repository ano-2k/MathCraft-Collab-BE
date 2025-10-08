# urls.py
from django.urls import path
from .views import RegisterAPIView, LoginAPIView
from .views import CreateGameModeView,CreateGameRecordsView,UpdateGameModeIQView
urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
   
   path('create-game/', CreateGameModeView.as_view(), name='create-game'),
   path('create-gameRecords/', CreateGameRecordsView.as_view(), name='create-gameRecords'),
   path('update-gameMode/<int:pk>/', UpdateGameModeIQView.as_view(), name='update-gameMode'),
]
