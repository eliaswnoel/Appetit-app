from django.urls import path, include
from . import views 

urlpatterns = [
  path('', views.home, name="home"),
  path('accounts/', include('django.contrib.auth.urls')),
  path('accounts/signup/', views.signup, name='signup'),
  path('recipes/create/', views.RecipeCreate.as_view(), name='recipes_create'),
  # path('recipes/<int:recipe_id>/add_review/', views.add_review, name='add_review'),
]
