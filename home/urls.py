from django.urls import path

from user.views import user_update
from . import views

urlpatterns = [
    path('home', views.index, name='index'),
    path('addcomment/<int:id>', views.addcomment, name='addcomment'),
    path('update/', views.user_update, name='user_update'),

]
