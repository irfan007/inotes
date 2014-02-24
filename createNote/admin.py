


from django.contrib import admin
from django.contrib.sites.models import Site
from createNote.models import Note
from django.contrib.auth.models import User, Group
from tinymce.widgets import TinyMCE

from django.forms import TextInput, Textarea
from django.db import models
class decorateNote(admin.ModelAdmin):
    list_display = ('title','category',)
    #list_display_links = ["user",]
    readonly_fields = ('owner', )
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': TinyMCE(attrs={'cols': 150, 'rows': 50})},
    }
        
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()

    
    def queryset(self, request):
        qs = super(decorateNote, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)



admin.site.register(Note,decorateNote)
#admin.site.unregister(User)
admin.site.unregister(Site)
admin.site.unregister(Group)