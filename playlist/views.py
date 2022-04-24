from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from neomodel import Traversal, match, config

config.DATABASE_URL = 'neo4j+s://neo4j:cgkKfYbz70cLGcTK6B7LnD4l7MjIVtD-hLTuZhTbRHI@712c260b.databases.neo4j.io:7687'

def index(request):
    
    return render(request, 'index.html', {
    
    })

def build_playlist(request):

    if request.method == 'POST':
        formset = PlayListTrackFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                album = form.cleaned_data.get('album')
                artist = form.cleaned_data.get('artist')
                title = form.cleaned_data.get('title')
                url = form.cleaned_data.get('url')
                if album or artist or title or url:
                    PlayList(album=album).save()
                    PlayList(artist=artist).save()
                    PlayList(title=title).save()
                    PlayList(url=url).save()

    playlist_form = PlayListForm(request.POST or None)
    playlisttrack_form = PlayListTrackForm(request.POST or None)
    playlisttag_form = PlayListTagForm(request.POST or None)
    playlistuser_form = PlayListUserForm(request.POST or None)
    playlistcountry_form = PlayListCountryForm(request.POST or None)

    if request.POST:
        if playlist_form.is_valid() and playlisttrack_form.is_valid() and playlisttag_form.is_valid() and playlistuser_form.is_valid() and playlistcountry_form.is_valid():
            playlist_title = playlist_form.cleaned_data.get("title")
            playlist_slug = playlist_form.cleaned_data.get("slug")
            track_album = playlisttrack_form.cleaned_data.get("album")
            track_artist = playlisttrack_form.cleaned_data.get("artist")
            track_title = playlisttrack_form.cleaned_data.get("title")
            track_url = playlisttrack_form.cleaned_data.get("url")
            tag = playlisttag_form.cleaned_data.get("name")
            user_country = playlistuser_form.cleaned_data.get("country")
            user_twitter = playlistuser_form.cleaned_data.get("twitter")
            country = playlistcountry_form.cleaned_data.get("name")
            
            merge_nodes (playlist_title, playlist_slug, track_album ,track_artist, track_title, track_url, tag, user_country, user_twitter, country) 
            
    context={
        'playlist_form':playlist_form,
        'playlisttrack_form':playlisttrack_form,
        'playlisttag_form':playlisttag_form,
        'playlistuser_form':playlistuser_form,
        'playlistcountry_form':playlistcountry_form,
            }
    
    return render(request, "build_playlist.html", context)

def view(request):

    playlist = PlayList.nodes.all()
    track = PlayListTracks.nodes.all()
    context={
        'playlist':playlist,
        'track':track
            }
   
    return render(request, "view_playlist.html", context)

def about(request):
    
    return render(request, 'about.html', {
        
    })
    
def contact(request):
    
    return render(request, 'contact.html', {
        
    })

def blog(request):
    
    return render(request, 'blog.html', {
        
    })

def elements(request):
    
    return render(request, 'elements.html', {
        
    })

def event(request):
    
    return render(request, 'event.html', {
        
    })

def features(request):
    
    return render(request, 'features.html', {
        
    })

def join(request):
    
    return render(request, 'join.html', {
        
    })

def pricing(request):
    
    return render(request, 'pricing.html', {
        
    })

def support(request):
    
    return render(request, 'support.html', {
        
    })

def team(request):
    
    return render(request, 'team.html', {
        
    })

def player(request):
    #tracks = Track.nodes.all()
    return render(request, 'player.html', {
        #'tracks': tracks
    })

# add another version of search that makes a path of tracks, same tags different countries

def search(request):
    try:
        q = request.GET["q"]
    except KeyError:
        return JsonResponse([])
    #here temporarily, we don't want to do this every time
    for tags_to_update in Tag.nodes.filter(name=q):
        tags_to_update.set_top_track()
            
    tags = Tag.nodes.filter(name=q).has(top_track=True)

    return JsonResponse([{
        'id': tag.uuid, 
        'title': tag.name, 
        'tagline': tag.top_track.single().title, 
        'released': tag.top_track.single().uuid, 
        'label': 'movie'
    } for tag in tags[:3]], safe=False)

def suggested_search(request):
    try:
        q = request.GET["q"]
    except KeyError:
        return JsonResponse([])
    
    #here temporarily, we don't want to do this every time
    for tags_to_update in Tag.nodes.filter(name__icontains=q):
        tags_to_update.suggested_track()
            
    tags = Tag.nodes.filter(name__icontains=q).has(related_from=True)
    return JsonResponse([{
        'id': tag.uuid, 
        'title': tag.name, 
        'tagline': tag.top_track.single().title, 
        'released': tag.top_track.single().uuid, 
        'label': 'movie'
    } for tag in tags[:]], safe=False)