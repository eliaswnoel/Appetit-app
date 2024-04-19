from django.urls import path 
from . import views 

urlpatterns = [
  path('', views.home, name="home"),
  path('', views.RecipeCreate.as_view(), name="recipe_create")
]
