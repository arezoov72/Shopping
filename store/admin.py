

from django.db.models.query import QuerySet
from django.contrib import admin

from tags.models import TaggedItem
from . import models
#in order to link an obj to dynamic app url
from django.urls import reverse
#in order to link an obj to url
from django.utils.html import format_html,urlencode
from django.db.models.aggregates import Count


# Register your models here.


#create custom filter
class InventoryFilter(admin.SimpleListFilter):
    title='inventory'
    parameter_name= 'inventory'

    def lookups(self,request,model_admin):
        return [
            ('<10','Low')
        
        ]

    #implementing filter
    def queryset(self, request, queryset:QuerySet):
        if self.value()=='<10':
            return queryset.filter(inventory__lt=10)
        



@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    #adding new action to pruduct
    actions=['clear_inventory']
    #readonly_fields,fields,exclude(to describe when adding new product)
    autocomplete_fields=['collection']
    prepopulated_fields={
        'slug':['title']
    }
    
    list_display=['title','unit_price','inventory_status','collection']
    list_filter=['collection','last_update',InventoryFilter]
    list_editable=['unit_price']
    list_per_page=10
    list_select_related=['collection']
    search_fields=['title']

    @admin.display(ordering='inventory')
    def inventory_status(self,product):
        if product.inventory<10:
            return "Low"
        return "OK"

    @admin.action(description='clear inventory')    
    def clear_inventory(self,request,queryset:QuerySet):
        updated_count=queryset.update(inventory=0)
        #give message after update
        self.message_user(
            request,
            f'{updated_count} products were updated successfully'
        )



@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display=['title','products_count']
    search_fields=['title']
    @admin.display(ordering='products_count')
    def products_count(self,collection):
        #reverse('admin:app_model_page')
        #changelist is the name of admin product changelist page
        url=(reverse('admin:store_product_changelist') 
        + '?'
        + urlencode({
            'collection_id':str(collection.id)
        }

        ))
        return format_html('<a href="{}">{}</a>',url,collection.products_count)
        
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count= Count('product')
        )

@admin.register(models.Customer)
class customerAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','membership','orders_count']
    search_fields= ['first_name','last_name']
    ordering=['first_name','last_name']
    list_editable=['membership']
    search_fields= ['first_name__istartswith','last_name__istartswith']
    list_per_page=10


    @admin.display(ordering='orders_count')
    def orders_count(self,customer):
        #reverse('admin:app_model_page')
        #changelist is the name of admin product changelist page
        url=(reverse('admin:store_order_changelist') 
        + '?'
        + urlencode({
            'customer_id':str(customer.id)
        }

        ))
        return format_html('<a href="{}">{}</a>',url,customer.orders_count)
        
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count= Count('order')
        )


#in order to have children inline in models 
#we can have TabularInline witch represent not seprately the order items or 
#stackedinline wich is seprated
class orderitemInline(admin.TabularInline):
    autocomplete_fields=['product']
    model=models.OrderItem

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['id','placed_at','customer']
    inlines=[orderitemInline]
    autocomplete_fields=['customer']
    
    
    list_per_page=10
    




# admin.site.register(models.Collection)
