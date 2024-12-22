from django.urls import path
from .views import GameView, IndexView, clear_session, results


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('game/', GameView.as_view(), name='game'),
    path('clear-session/', clear_session, name='clear_session'),
    path('results/', results, name='results'),
]