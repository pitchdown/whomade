from django.shortcuts import render
from django.views import View
from user.models import User


# Create your views here.

class LeaderboardView(View):
    def get(self, request):
        leaderboard = User.objects.all()
        leaderboard = sorted(leaderboard, key=lambda p: p.average_guess, reverse=True)
        return render(request, 'leaderboard.html', {'leaderboard': leaderboard})
