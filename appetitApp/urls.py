from django.urls import path, include
from . import views 

urlpatterns = [
  path('', views.home, name="home"),
  path('accounts/', include('django.contrib.auth.urls')),
  # 7 authentication
  path('accounts/signup/', views.signup, name='signup'),
  
  # 8 RecipeCreate
  path('recipes/create/', views.RecipeCreate.as_view(), name='recipes_create'),
  
  # 6 recipes_detail - API
  path('recipes/<int:recipe_id>/', views.recipes_detail, name='detail'),
  
  # 1 recipes_index - show all recipes a user has searched for 
  path('recipes/', views.recipes_index, name='index'),
  
  # path('recipes/', views.recipes_user_recipe, name='user_recipe'),
  
  # 9 RecipeUpdated 
  path('recipes/<int:pk>/update/', views.RecipeUpdate.as_view(), name='recipes_update'),
  
  # 10 RecipeDelete
  path('recipes/<int:pk>/delete/', views.RecipeDelete.as_view(), name='recipes_delete'),
  
  # 2 recipes_user_recipe - shows the recipe detail page of a recipe that a user created
  path('recipes/user/<int:recipe_id>/', views.recipes_user_recipe, name='user_recipe'),
  
  # 4 add_ingredients - user adds ingredients to their recipe
  path('recipes/<int:recipe_id>/add_ingredient/', views.add_ingredient, name='add_ingredient'), 
  
  #  3 add_review user adds a review to a recipe
  path('recipes/<int:recipe_id>/add_review/', views.add_review, name='add_review'), 
  
  # 5 add_step - user adds steps to a recipe
  path('recipes/<int:recipe_id>/add_steps', views.add_steps, name="add_steps"),
  
  # 11 FolderList - view folders that user created 
  path('folders/', views.FolderList.as_view(), name='folders_index'),
  
  # 12 FolderCreate - user creates a folder
  path('folders/create/', views.FolderCreate.as_view(), name='folders_create'),
  path('folders/<int:folder_id>/', views.folders_detail, name='folders_detail'),
  path('folders/<int:pk>/update/', views.FolderUpdate.as_view(), name='folders_update'),
  path('folders/<int:pk>/delete/', views.FolderDelete.as_view(), name='folders_delete'),

]