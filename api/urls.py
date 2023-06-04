from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'fooditem', views.FoodItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('recommendfood/', views.recommendfood),
    path('foodrec/', views.foodrec),
    path('waterrec/', views.waterrec),
    path('sleeprec/', views.sleeprec),
    path('menu/', views.menu)
]
