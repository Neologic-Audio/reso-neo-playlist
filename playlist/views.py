from django.shortcuts import render, redirect
from .models import *
from .forms import PlayListCountryForm, PlayListForm, PlayListTrackForm, PlayListTagForm, PlayListUserForm
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from neomodel import Traversal, match

def index(request):
    
    return render(request, 'index.html', {
    
    })

def build_playlist(request):
    playlist_form = PlayListForm(request.POST or None)
    playlisttrack_form = PlayListTrackForm(request.POST or None)
    playlisttag_form = PlayListTagForm(request.POST or None)
    playlistuser_form = PlayListUserForm(request.POST or None)
    playlistcountry_form = PlayListCountryForm(request.POST or None)

    if playlist_form.is_valid():
        playlist_form.save()
    
    if playlisttrack_form.is_valid():
        playlisttrack_form.save()

    if playlisttag_form.is_valid():
        playlisttag_form.save()

    if playlistuser_form.is_valid():
        playlistuser_form.save()

    if playlistcountry_form.is_valid():
        playlistcountry_form.save()

    
    
    
    context={
        'playlist_form':playlist_form,
        'playlisttrack_form':playlisttrack_form,
        'playlisttag_form':playlisttag_form,
        'playlistuser_form':playlistuser_form,
        'playlistcountry_form':playlistcountry_form,
            }


    messages.success(request, ('Track has been Added'))
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


# Makes the cute graph UI
def graph(request):
    nodes = []
    rels = []
    tags = Tag.nodes.has(top_track=True)

    i = 0
    for tag in tags:
        nodes.append({'id': tag.uuid, 'title': tag.name, 'label': 'tag'})
        target = i
        i += 1

        for trackgroup in tag.has_tag:
            group = {'id': trackgroup.uuid, 'title': trackgroup.title, 'label': 'group'}

            try:
                source = nodes.index(group)
            except ValueError:
                nodes.append(group)
                source = i
                i += 1
            rels.append({"source": source, "target": target})

    return JsonResponse({"nodes": nodes, "links": rels})

# add another version of search that makes a path of tracks, same tags different countries

def search(request):
    try:
        q = request.GET["q"]
    except KeyError:
        return JsonResponse([])

    #here temporarily, we don't want to do this every time
    for tags_to_update in Tag.nodes.filter(name__icontains=q):
        tags_to_update.set_top_track()

    tags = Tag.nodes.filter(name__icontains=q).has(top_track=True)
    return JsonResponse([{
        'id': tag.uuid, 
        'title': tag.name, 
        'tagline': tag.top_track.single().title, 
        'released': tag.top_track.single().uuid, 
        'label': 'movie'
    } for tag in tags], safe=False)
