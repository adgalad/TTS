"""TTS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static

from app import views
from TTS.settings import MEDIA_URL, MEDIA_ROOT

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', views.index, name="index"),
    
    url(r'^login/$', views.User.login, name="login"),
    url(r'^signup/$', views.User.signup, name="signup"),
    url(r'^logout/$', views.User.logout, name="logout"),
    url(r'^profile/$', views.User.profile, name="profile"),

    url(r'^audios/$', views.Audio.list, name="audios"),
    url(r'^audio/new$', views.Audio.new, name="newAudio"),
    url(r'^audio/create$', views.Audio.create, name="createAudio"),
    url(r'^audio/edit/(?P<pk>\d+)$', views.Audio.edit, name="editAudio"),
    url(r'^list/review$', views.Audio.listReview, name="listReview"),
    url(r'^list/review/(?P<success>\d+)$', views.Audio.listReview, name="listReview"),
    url(r'^audio/review/(?P<pk>\d+)$', views.Audio.review, name="review"),
    url(r'^audio/delete/(?P<pk>\d+)$', views.Audio.reject, name="rejectAudio"),
    url(r'^audio/accept/(?P<pk>\d+)$', views.Audio.accept, name="aceceptAudio"),
    url(r'^audio/accept/(?P<pk>\d+)$', views.Audio.accept, name="aceceptAudio"),

    url(r'^api/processAudio/test\.mp3$', views.TTS.process, name="processAudio")

] + static(MEDIA_URL, document_root=MEDIA_ROOT)
