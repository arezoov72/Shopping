from django.contrib import admin
#in order to add generic relashion from another app in this
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProductAdmin
from store.models import Product
from tags.models import TaggedItem
# Register your models here.

class TagInlines(GenericTabularInline):
    model= TaggedItem
    autocomplete_fields=['tag']



class CustomProductAdmin(ProductAdmin):
    inlines=[TagInlines]


admin.site.unregister(Product)
admin.site.register(Product,CustomProductAdmin)


#with this Tag and store can be seprated and if suddenly store_custom be deleted
#nothing will happen except we can have product without tags