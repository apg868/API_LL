from django.contrib import admin
from django.urls import path, include
from . import views
from . import models

urlpatterns = [
    path('categories/', views.CategoriesView.as_view ()),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('menu-items', views.menu_items),
]