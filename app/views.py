import json
import datetime
import requests

from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as login_auth
from django.contrib.auth import logout as logout_auth
from django.http import JsonResponse
from django.http import HttpResponseServerError
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from app import models, forms
from .watson_text_to_speech import text_to_specch

# Create your views here.

@login_required(login_url="/login")
def index(request):
  return redirect('audios')

class User:
  def login(request):
    if request.method == "POST":
      form = forms.Login(request.POST)
      if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
          login_auth(request, user)
          return redirect(request.GET.get('next',reverse('index')))
        else:
          messages.error(request, "Bad email or password.")
    else:
      form = forms.Login()
    return render(request, "login.html", {'form': form})    

  def logout(request):
    logout_auth(request)
    return redirect(reverse('login'))

  def signup(request):
    if request.method == "POST":
      POST = request.POST.copy()
      POST['created_by'] = request.user
      form = forms.SignUp(POST)
      if form.is_valid():
        #print(form.cleaned_data)
        form.save()
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=email, password=password)
        if user is not None:
          login_auth(request, user)
          return redirect(reverse('index'))
    else:
      form = forms.SignUp()
    
    return render(request, "form.html", {'form': form})

  def profile(request):
    return render(request, "profile.html")    
    

class TTS:

  @login_required(login_url="/login")
  @csrf_exempt
  def process(request):
    data = request.GET
    if request.method != "GET" or not 'text' in data:
      return HttpResponseServerError
    if not data['text']:
      return HttpResponseServerError
    return text_to_specch.processRequest(data['text'])


class Audio:
  def get(pk):
    try:
      audio = models.Audio.objects.get(pk=pk)
    except Exception as e:
      raise PermissionDenied
    return audio

  @login_required(login_url="/login")
  def new(request):
    if request.method == "POST":
      form = forms.NewAudio(request.POST, request.FILES)
      form.fields['audio'].queryset = request.user.audios.all()
      if form.is_valid():
        type = form.cleaned_data['type']
        if type == "new":
          return redirect('/audio/create')
        elif type == "existant":
          return redirect('/audio/create?text='+form.cleaned_data['audio'].text)
        else:
          text = form.cleaned_data['file']
          return redirect('/audio/create?text='+text)

    else:
      form = forms.NewAudio()
      form.fields['audio'].queryset = request.user.audios.all()
    return render(request, "new_audio.html", {'form': form})

  @login_required(login_url="/login")
  def create(request):
    if request.method == "POST":
      form = forms.CreateAudio(request.POST)
      if form.is_valid():
        record = form.save()
        record.created_by = request.user
        record.save()
        record.createAudio()

        return redirect('/')
      else:
        return render(request, "create_audio.html", {"form": form, 'title':'Crear audio'})
    text = request.GET.get('text', '')

    if text:
      form = forms.CreateAudio(initial={"text":text})
    else:
      form = forms.CreateAudio()
    return render(request, "create_audio.html", {"form": form, 'title':'Crear audio'})

  @login_required(login_url="/login")
  def edit(request, pk):
    audio = Audio.get(pk)
    if audio.status == "Aprobado":
      raise PermissionDenied
    if request.method == "POST":
      form = forms.CreateAudio(request.POST, instance=audio)
      if form.is_valid():
        record = form.save()
        record.createAudio()
        return redirect('/')
      else:
        return render(request, "create_audio.html", {"form": form, 'title':'Modificar audio'})    
    else:
      form = forms.CreateAudio(instance=audio)
    return render(request, "create_audio.html", {"form": form, 'audio': audio, 'title':'Modificar audio'})

  def list(request):
    return render(request, "audios.html", {
        "audios": request.user.audios.all().order_by('-created_at')
      })

  def listReview(request, success=False):
    return render(request, "list_review.html", {
        "audios":models.Audio.objects.filter(status="En revisión").order_by('-created_at'), 
        'success':success
      })

  def review(request, pk):
    audio = Audio.get(pk)
    if audio.status == "Aprobado":
      raise PermissionDenied
    return render(request, "review_audio.html", {"audio": audio})

  def reject(request, pk):
    audio = Audio.get(pk)
    audio.delete()
    return redirect("listReview")    

  def accept(request, pk):
    audio = Audio.get(pk)
    if audio.status == "Aprobado":
      raise PermissionDenied

    audio.status = "Aprobado"
    audio.save()
    return redirect("listReview", '1')


