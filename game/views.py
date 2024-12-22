from PIL import ImageFilter, Image
from io import BytesIO
import requests
import base64
import os
from django.conf import settings

from django.shortcuts import render, redirect
from django.views import View
from rest_framework.views import APIView
import random
from spotify_api.models import Album, Artist
from django.http import JsonResponse
from .tasks import fetch_album_data
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from user.models import User


class IndexView(APIView):
    def get(self, request):
        if 'game_data' in request.session:
            del request.session['game_data']

        media_path = os.path.join(settings.BASE_DIR, 'static', 'media')
        image_files = [f for f in os.listdir(media_path) if f.endswith(('jpg', 'jpeg', 'png', 'gif'))]
        random_image = random.choice(image_files)
        return render(request, 'index.html', {'random_image': random_image})


@method_decorator(login_required, name='dispatch')
class GameView(View):
    def get(self, request):
        if 'game_data' not in request.session:
            result = fetch_album_data.apply_async()

            game_data = result.get()
            request.session['game_data'] = game_data
            request.session['current_index'] = 0
            request.session['game_results'] = {'is_correct': 0, 'is_false': 0}
            request.session.modified = True

        current_index = request.session['current_index']
        game_data = request.session['game_data'][current_index]

        context = {
            'album_name': game_data['album_name'],
            'album_image': game_data['album_image'],
            'artists': game_data['artists'],
            'current_round': current_index + 1,
            'total_rounds': len(request.session['game_data']),
            'game_results': request.session['game_results']
        }

        return render(request, 'game.html', context)

    def post(self, request):
        selected_artist = request.POST.get('artist_name')
        current_index = request.session['current_index']
        correct_artist = request.session['game_data'][current_index]['correct_artist']

        if selected_artist == correct_artist:
            request.session['game_results']['is_correct'] += 1
            request.user.correct_answers += 1
        else:
            request.session['game_results']['is_false'] += 1
            request.user.wrong_answers += 1

        request.user.total_questions += 1
        request.user.save()

        request.session['current_index'] += 1
        request.session.modified = True

        if request.session['current_index'] >= len(request.session['game_data']):
            return redirect('results')

        return redirect('game')


def results(request):
    results = request.session.get('game_results', {'is_correct': 0, 'is_false': 0})

    request.session.pop('game_data', None)
    request.session.pop('current_index', None)
    request.session.pop('game_results', None)
    request.session.modified = True

    return render(request, 'results.html', {'results': results})


def clear_session(request):
    request.session.flush()
    return redirect('game')
