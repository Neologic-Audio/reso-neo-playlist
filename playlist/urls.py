from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('player/', views.player, name="player"),
    path('build_playlist/', views.build_playlist, name="build_playlist"),
    path('view_playlist/', views.view, name="view_playlist"),
    path('about/', views.about, name="about"),
    path('team/', views.team, name="team"),
    path('404', views.handler404, name="404"),
    path('500', views.handler500, name="500"),
]
