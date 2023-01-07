from django.urls import path
from .views import index, detail, create, edit, delete

app_name = 'articles'

urlpatterns = [
    path('', index, name="list"),
    path('article/<slug:slug>/', detail, name="detail"),
    path('article/d/create/', create, name="create"),
    path('article/edit/<slug:slug>/', edit, name="edit"),
    path('article/delete/<slug:slug>/', delete, name="delete"),
]