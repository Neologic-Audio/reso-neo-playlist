from django.core.mail.backends import console
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from neomodel import Traversal, match, config


def index(request):
    return render(request, 'index.html', {

    })


def build_playlist(request):
    if request.method == 'POST':
        formset = PlayListTrackFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                title = form.cleaned_data.get('title')
                if title:
                    PlayList(title=title).save()

    playlist_form = PlayListForm(request.POST or None)
    playlisttrack_form = PlayListTrackForm(request.POST or None)
    playlisttag_form = PlayListTagForm(request.POST or None)


    if request.POST:
        if playlist_form.is_valid() and playlisttrack_form.is_valid() and playlisttag_form.is_valid():
            playlist_title = playlist_form.cleaned_data.get("title")
            track_title = playlisttrack_form.cleaned_data.get("track")
            tag = playlisttag_form.cleaned_data.get("name")

           
            merge_nodes(playlist_title, track_title, tag)

    context = {
        'playlist_form': playlist_form,
        'playlisttrack_form': playlisttrack_form,
        'playlisttag_form': playlisttag_form,
    }

    return render(request, "build_playlist.html", context)


def view(request):
    playlist = PlayList.nodes.all()
    track = PlayListTracks.nodes.all()
    context = {
        'playlist': playlist,
        'track': track
    }

    return render(request, "view_playlist.html", context)


def about(request):
    return render(request, 'about.html', {

    })


def team(request):
    return render(request, 'team.html', {

    })


def player(request):
    # tracks = Track.nodes.all()
    return render(request, 'player.html', {
        # 'tracks': tracks
    })


# add another version of search that makes a path of tracks, same tags different countries

def search(request):
    try:
        q = request.GET["q"]
    except KeyError:
        return JsonResponse([])
    # here temporarily, we don't want to do this every time
    for tags_to_update in Tag.nodes.filter(name=q):
        tags_to_update.set_top_track()

    tags = Tag.nodes.filter(name=q).has(top_track=True)

    return JsonResponse([{
        'id': tag.uuid,
        'title': tag.name,
        'tagline': tag.top_track.single().title,
        'released': tag.top_track.single().uuid,
        'label': 'track'
    } for tag in tags[:3]], safe=False)


def suggested_search(request):
    try:
        q = request.GET["q"]
    except KeyError:
        return JsonResponse([])

    # here temporarily, we don't want to do this every time
    for tags_to_update in Tag.nodes.filter(name__icontains=q):
        tags_to_update.suggested_track()

    tags = Tag.nodes.filter(name__icontains=q).has(related_from=True)
    return JsonResponse([{
        'id': tag.uuid,
        'title': tag.name,
        'tagline': tag.top_track.single().title,
        'released': tag.top_track.single().uuid,
        'label': 'track'
    } for tag in tags[:]], safe=False)


def search_playlists(request):
    try:
        q = request.GET["q"]
    except KeyError:
        return JsonResponse([])

    # # here temporarily, we don't want to do this every time
    # for tags_to_update in Tag.nodes.filter(name=q):
    #     tags_to_update.import_playlists()

    track = TrackGroup.nodes.filter(name=q).has(has_track=True)

    return JsonResponse([{
        'id': track.id,
        'title': track.title,
        'track name': track.title,
        'track id': track.id,
        'label': 'tracks'
    } for track in Track[:]], safe=False)


def handler404(request, *args, **argv):
    return render(request, '404.html', {
    })


def handler500(request, *args, **argv):
    return render(request, '500.html', {
    })
