from django.urls import path

from tables import views

urlpatterns = [
    path('bar/',views.bars,name='bar'),
    path('pie/',views.pie,name='pie'),
    path('map/',views.maps,name='map'),

]