from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('player/', views.player, name="player"),
    path('build_playlist/', views.build_playlist, name="build_playlist"),
    path('view_playlist/', views.view, name="view_playlist"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('blog/', views.blog, name="blog"),
    path('elements/', views.elements, name="elements"),
    path('event/', views.event, name="event"),
    path('features/', views.features, name="features"),
    path('join/', views.join, name="join"),
    path('pricing/', views.pricing, name="pricing"),
    path('support/', views.support, name="support"),
    path('team/', views.team, name="team"),
    path('404', views.handler404, name="404"),
    path('500', views.handler500, name="500"),
]
