from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey



#what users liked what obj
# Create your models here.

class LikedItem(models.Model):
    content_type=models.ForeignKey(User,on_delete=CASCADE)
    #identify user likes
    content_type=models.ForeignKey(ContentType,on_delete=CASCADE)
    #refrence the obj
    object_id=models.PositiveIntegerField()
    #reading obj
    content_object=GenericForeignKey()






