from django.forms import ModelForm
from django_neomodel import DjangoNode
from .models import PlayList, PlayListTracks, PlayListTag, PlayListUser, PlayListCountry
from neomodel import *

config.DATABASE_URL = 'neo4j+s://neo4j:cgkKfYbz70cLGcTK6B7LnD4l7MjIVtD-hLTuZhTbRHI@712c260b.databases.neo4j.io:7687'


class PlayListForm(ModelForm):
    has_tag = RelationshipTo('PlayListTag', 'HAS_TAG')
    has_track = RelationshipTo('PlayListTracks', 'HAS_TRACK')
    owns = RelationshipFrom('PlayListUser', 'OWNS')

    class Meta:
        model = PlayList
        fields = ['playlist_title']


class PlayListTrackForm(ModelForm):
    has_track = RelationshipFrom('PlayListTracks', 'HAS_TRACK')

    class Meta:
        model = PlayListTracks
        fields = ['track_title']


class PlayListTagForm(ModelForm):
    has_tag = RelationshipFrom('PlayList', 'HAS_TAG')
    top_track = RelationshipTo('PlayListTracks', 'TOP_TRACK')
    related_to = RelationshipTo('PlayListTag', 'RELATED')
    related_from = RelationshipFrom('PlayListTag', 'RELATED')

    class Meta:
        model = PlayListTag
        fields = ['tag_name']


class PlayListUserForm(ModelForm):
    owns = RelationshipTo('PlayList', 'OWNS')

    class Meta:
        model = PlayListUser
        fields = ['user_name']


class PlayListCountryForm(ModelForm):
    in_country = RelationshipFrom('PlayListUser', 'IN_COUNTRY')

    class Meta:
        model = PlayListCountry
        fields = ['country_name']

