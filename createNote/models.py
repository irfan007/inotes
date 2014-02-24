from django.db import models

# Create your models here.

#from tinymce.models import HTMLField

from django.contrib.auth.models import User
from datetime import datetime 

class Note(models.Model):
    owner=models.ForeignKey(User,null=True,blank=True)
    title=models.CharField(max_length=500)
    keywords=models.CharField(max_length=500)
    category=models.CharField(max_length=100)
    content = models.TextField()
    last_edit=models.DateField(blank=True,null=True)
    
    
    def __unicode__(self):
        return self.title+":"+self.category+":"+self.keywords
    
    
    def validate_unique(self, *args, **kwargs):
        super(Note, self).validate_unique(*args, **kwargs)
        self.last_edit=datetime.today()
        
#     
        
    
   
    

