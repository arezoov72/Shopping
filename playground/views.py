import imp
from unicodedata import decimal
from django.forms import DecimalField
from django.shortcuts import render
#from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F,ExpressionWrapper
from django.db.models.aggregates import Count

from store.models import Product,OrderItem





def say_hello(request):
    #we can add another models atribute here
    # queryset=Product.objects.filter(collection__id__range=(1,5))
    #select_related  if we want  (1) object
    #prefetch_related if we want (n) objects(many to many relashions)
    #to have list of product that have been orderd queryset
    
    queryset=Product.objects.filter(id__in=
    OrderItem.objects.values('product_id').distinct()).order_by('title')
    result=Product.objects.aggregate(count=Count('id'))
    discounted_price=ExpressionWrapper(F('unit_price')*0.8,output_field=DecimalField())
    q1=Product.objects.annotate(discounted_price=discounted_price)

    #Prodects: inventory=price
    q2=Product.objects.filter(inventory=F("unit_price"))

  

    return render(request, 'hello.html', {'name': 'Arezoo','products':list(queryset),'result':result})

