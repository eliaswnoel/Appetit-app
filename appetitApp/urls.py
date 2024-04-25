from django.urls import path, include
from . import views 

urlpatterns = [
  path('', views.home, name="home"),
  path('accounts/', include('django.contrib.auth.urls')),
  # 1 recipes_index - show all recipes a user has searched for 
  path('recipes/', views.recipes_index, name='index'),
  # 2 recipes_user_recipe - shows the recipe detail page of a recipe that a user created
  path('recipes/user/<int:recipe_id>/', views.recipes_user_recipe, name='user_recipe'),
  #  3 add_review user adds a review to a recipe
  path('recipes/<int:recipe_id>/add_review/', views.add_review, name='add_review'), 
  path('recipes/<int:recipe_id>/add_review/', views.add_review_api, name='add_review_api'), 
  # 4 add_ingredients - user adds ingredients to their recipe
  path('recipes/<int:recipe_id>/add_ingredient/', views.add_ingredient, name='add_ingredient'), 
  # 5 add_step - user adds steps to a recipe
  path('recipes/<int:recipe_id>/add_steps', views.add_steps, name="add_steps"),
  # 6 recipes_detail - API
  path('recipes/<int:recipe_id>/', views.recipes_detail, name='detail'),
  # 7 authentication
  path('accounts/signup/', views.signup, name='signup'),
  # 8 RecipeCreate
  path('recipes/create/', views.RecipeCreate.as_view(), name='recipes_create'),
  # 9 RecipeUpdated 
  path('recipes/<int:pk>/update/', views.RecipeUpdate.as_view(), name='recipes_update'),
  # 10 RecipeDelete
  path('recipes/<int:pk>/delete/', views.RecipeDelete.as_view(), name='recipes_delete'),
  # 11 FolderList - view folders that user created 
  path('folders/', views.FolderList.as_view(), name='folders_index'),
  # 12 FolderCreate - user creates a folder
  path('folders/create/', views.FolderCreate.as_view(), name='folders_create'),
  # 13 Search functionality 
  path('search/', views.search_recipes, name="search_recipes"),
  # 14 folders details
  path('folders/<int:folder_id>/', views.folders_detail, name='folders_detail'),
  # 15 folders update
  path('folders/<int:pk>/update/', views.FolderUpdate.as_view(), name='folders_update'),  
  #  16 folders delete
  path('folders/<int:pk>/delete/', views.FolderDelete.as_view(), name='folders_delete'),
  # delete review
  path('recipes/<int:recipe_id>/reviews_delete/<int:pk>/', views.ReviewDelete.as_view(), name='reviews_delete'),
  # edit review
  path('recipes/<int:recipe_id>/reviews/<int:pk>/edit/', views.ReviewUpdate.as_view(), name='reviews_edit'),
  path('recipes/<int:recipe_id>/add_photo/', views.add_photo, name='add_photo'),
  path('recipes/user/<int:recipe_id>/assoc_folder/<int:folder_id>', views.assoc_folder, name="assoc_folder"),
  path('recipes/user/profile/', views.create_user_profile, name='create_profile')
]