from django.forms import ModelForm, formset_factory
from .models import PlayList, PlayListTracks, PlayListTag, PlayListUser, PlayListCountry, merge_nodes


class PlayListForm(ModelForm):
    class Meta:
        model = PlayList
        fields = ['Title']


class PlayListTrackForm(ModelForm):
    class Meta:
        model = PlayListTracks
        fields = ['Track']


class PlayListTagForm(ModelForm):
    class Meta:
        model = PlayListTag
        fields = ['Name']


# class PlayListUserForm(ModelForm):
#     class Meta:
#         model = PlayListUser
#         # fields = ['country', 'twitter']
#
#
# class PlayListCountryForm(ModelForm):
#     class Meta:
#         model = PlayListCountry
#         # fields = ['name']


PlayListTrackFormSet = formset_factory(PlayListTrackForm, extra=1)