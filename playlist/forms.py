from django.forms import ModelForm
from .models import PlayList, PlayListTracks, PlayListTag, PlayListUser, PlayListCountry, merge_nodes

class PlayListForm(ModelForm):
   
    class Meta:
        model = PlayList
        fields = ['title']

class PlayListTrackForm(ModelForm):
 
    class Meta:
       
        model = PlayListTracks
        fields = ['track']

class PlayListTagForm(ModelForm):
    
    class Meta:
        
        model = PlayListTag
        fields = ['tag']

class PlayListUserForm(ModelForm):
    
    class Meta:
        
        model = PlayListUser
        fields = ['user']

class PlayListCountryForm(ModelForm):
    
    class Meta:
        
        model = PlayListCountry
        fields = ['country']



