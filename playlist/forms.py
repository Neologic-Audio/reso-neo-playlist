from django.forms import ModelForm
from .models import PlayList, PlayListTracks, PlayListTag, PlayListUser, PlayListCountry

class PlayListForm(ModelForm):
    class Meta:
        model = PlayList
        fields = ['playlist_title']

class PlayListTrackForm(ModelForm):
    class Meta:
        model = PlayListTracks
        fields = ['track_title']

class PlayListTagForm(ModelForm):
    class Meta:
        model = PlayListTag
        fields = ['tag_name']

class PlayListUserForm(ModelForm):
    class Meta:
        model = PlayListUser
        fields = ['user_name']

class PlayListCountryForm(ModelForm):
    class Meta:
        model = PlayListCountry
        fields = ['country_name']
