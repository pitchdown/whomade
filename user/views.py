import requests
import base64
import time

from rest_framework.views import APIView
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout

from whomade.settings import CLIENT_ID, CLIENT_SECRET
from .forms import UserSignInForm, UserSignUpForm
from .serializers import UserRegisterSerializer, UserLoginSerializer
from spotify_api.models import SpotifyToken
from user.models import User
from django.contrib.auth.decorators import login_required



class UserSignUpView(View):
    def get(self, request, *args, **kwargs):
        form = UserSignUpForm()
        return render(request, 'sign_up.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(email, username, password)
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return redirect('signin')
        return render(request, 'sign_up.html', {'form': form})


class UserSignInView(APIView):
    def get(self, request, *args, **kwargs):
        form = UserSignInForm()
        return render(request, 'sign_in.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserSignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)

                url = 'https://accounts.spotify.com/api/token'
                headers = {'Authorization': 'Basic ' + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()}
                data = {'grant_type': 'client_credentials'}
                response = requests.post(url, headers=headers, data=data)
                access_token = response.json()['access_token']
                expires_at = time.time() + response.json()['expires_in']

                SpotifyToken.objects.create(token=access_token, expires_at=expires_at)

                return redirect('/')

            else:
                return render(request, 'sign_in.html', {'form': form, 'error': 'Invalid credentials.'})

        return render(request, 'sign_in.html', {'form': form})



class UserLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)

        if request.session.get('access_token'):
            del request.session['access_token']

        return Response({"message": "Successfully logged out."}, status=200)


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'profile.html', {
        'user': user,
        'correct_answers': user.correct_answers,
        'wrong_answers': user.wrong_answers,
        'total_questions': user.total_questions
    })