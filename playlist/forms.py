from django.forms import ModelForm, formset_factory
from .models import PlayList, PlayListTracks, PlayListTag, PlayListUser, PlayListCountry, merge_nodes


class PlayListForm(ModelForm):
    class Meta:
        model = PlayList
        fields = ['title']


class PlayListTrackForm(ModelForm):
    class Meta:
        model = PlayListTracks
        fields = ['title']


class PlayListTagForm(ModelForm):
    class Meta:
        model = PlayListTag
        fields = ['name']


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