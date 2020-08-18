from django.http import HttpResponse
from django.urls import path
from product import views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addcomment/<int:id>', views.addcomment, name='addcomment'),
]


