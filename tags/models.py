from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.

class Tag(models.Model):
    lable=models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.lable


class TaggedItem(models.Model):
    #what tagapplied to what obj
    tag=models.ForeignKey(Tag,on_delete=CASCADE)
    #Type (product,video,article)
    #ID
    content_type=models.ForeignKey(ContentType,on_delete=CASCADE)
    object_id=models.PositiveIntegerField()
    #to read contentTypes
    content_object=GenericForeignKey()