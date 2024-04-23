from django.urls import path, include
from . import views 

urlpatterns = [
  path('', views.home, name="home"),
  path('accounts/', include('django.contrib.auth.urls')),
  path('accounts/signup/', views.signup, name='signup'),
  path('recipes/create/', views.RecipeCreate.as_view(), name='recipes_create'),
  path('recipes/<int:recipe_id>/', views.recipes_detail, name='detail'),
  path('recipes/', views.recipes_index, name='index'),
  path('recipes/', views.recipes_user_recipe, name='user_recipe'),
  path('recipes/<int:pk>/update/', views.RecipeUpdate.as_view(), name='recipes_update'),
  path('recipes/<int:pk>/delete/', views.RecipeDelete.as_view(), name='recipes_delete'),
  path('recipes/user/<int:recipe_id>/', views.recipes_user_recipe, name='user_recipe'),
  path('recipes/<int:recipe_id>/add_ingredient/', views.add_ingredient, name='add_ingredient'), 
  path('recipes/<int:recipe_id>/add_review/', views.add_review, name='add_review'), 
  path('recipes/<int:recipe_id>/add_steps', views.add_steps, name="add_steps"),
  path('folders/', views.FolderList.as_view(), name='folders_index'),
  path('folders/create/', views.FolderCreate.as_view(), name='folders_create'),
]