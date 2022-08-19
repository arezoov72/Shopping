from cgitb import lookup
from unicodedata import name
from django.urls import path
from . import views
from rest_framework_nested import routers


from rest_framework.routers import SimpleRouter


router=routers.DefaultRouter()
router.register('products',views.ProductViewSet,basename='products'),
router.register('collections',views.CollectionViewSet)
router.register('carts',views.CartViewset)

#child
product_router=routers.NestedDefaultRouter(router,'products',lookup='product')
#childresource
product_router.register('reviews',views.ReviewViewSet,basename='product-reviews ')


# URLConf
urlpatterns = router.urls + product_router.urls
# [ 
#     path('products/', views.ProductList.as_view()),
#     path('products/<int:pk>', views.ProductDetail.as_view()),
#     path('collections/', views.CollectionList.as_view()),
#     path('collections/<int:pk>', views.CollectionDetail.as_view(),name='collection_detail')
# ]