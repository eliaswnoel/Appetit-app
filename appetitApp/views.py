import uuid
import os
import boto3
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Recipe, Folder, Review, Photo
from .forms import ReviewForm, IngredientForm, StepsForm, RecipeForm
from .api_manage import accessAPI, fetch_recipe_from_api
from django.urls import reverse_lazy
from django.conf import settings

recipe_list = '/recipes/list'
tags_list = '/tags/list'
get_recipe = '/recipes/get-more-info'

# homepage view
def home(request): 
  if not request.user.is_authenticated:
    return redirect(f'{settings.LOGIN_URL}?next={request.path}')
  # get most popular recipes
  popular_params = {'from': '0', 'size':'4','q':'lunch'}
  popular_api = accessAPI(recipe_list, popular_params, 'GET')
  popular_json = popular_api['results']
  user_recipes = Recipe.objects.all()
  # get cuisine types 
  cuisine_tags_api = accessAPI(tags_list, '', 'GET')
  cuisine_tags_json = cuisine_tags_api['results']

  tags_display = ('italian', 'mexican', 'greek', 'indian', 'thai', 'korean', 'jamaican', 'chinese', 'fusion', 'lebanese')

  return render(request, 'home.html', {
    'popular_recipes': popular_json,
    'cuisines': cuisine_tags_json,
    'user_recipes': user_recipes,
    'tags': tags_display
  })


# 13 Search functionality 
def search_recipes(request):
  recipe = request.POST['recipe']
  if request.method == "POST":
    params = {
      'from': '0',
      'size': 20,
      'q': recipe
    }
    recipe_api = accessAPI(recipe_list, params, "GET")
    recipe_json = recipe_api['results']
  return render(request, 'search.html', {'recipes': recipe_json, 'recipe_name': recipe})

# 1 view all recipes that a user searches for
def recipes_index(request, category_name):
  params ={
    'from': '0',
    'size': '20',
    'q': category_name
  },
  category_api = accessAPI(recipe_list, params, 'GET')
  category_json = category_api['results']
  folders = Folder.objects.all()
  
  return render(request, 'recipes/index.html', {
    'category': category_json, 
    'folders': folders
  })

# 2 direct to a user created recipe
def recipes_user_recipe(request, recipe_id):
  recipe = Recipe.objects.get(id=recipe_id)
  author = recipe.user
  ingredient_form = IngredientForm
  steps_form = StepsForm
  review_form = ReviewForm
  folders = Folder.objects.all()
    
  return render(request, 'recipes/user/user_recipe.html', {
    'recipe': recipe, 
    'ingredient_form': ingredient_form, 
    'steps_form': steps_form, 
    'review_form': review_form,
    'folders': folders,
    'author': author
  })

# 3 add review to recipe
def add_review(request, recipe_id):
  form = ReviewForm(request.POST)

  if form.is_valid():
    new_review = form.save(commit=False)
    new_review.recipe_id = recipe_id
    new_review.user = request.user
    new_review.save()
  return redirect('user_recipe', recipe_id=recipe_id)

# delete review from recipe
class ReviewDelete(DeleteView):
  model = Review
  success_url = '/recipes/user/{recipe_id}/'


  def delete(self, request, *args, **kwargs):
    self.object = self.get_object()
    self.object.delete()
    return redirect(self.get_success_url())


# 4 add ingredients to recipe
def add_ingredient(request, recipe_id):
  form = IngredientForm(request.POST)

  if form.is_valid():
    new_ingredient = form.save(commit=False)
    new_ingredient.recipe_id = recipe_id
    new_ingredient.save()
  return redirect('user_recipe', recipe_id=recipe_id)

# 5 add steps
def add_steps(request, recipe_id):
  form = StepsForm(request.POST)

  if form.is_valid():
    new_step = form.save(commit=False)
    new_step.recipe_id = recipe_id
    new_step.save()
  return redirect('user_recipe', recipe_id=recipe_id)

# 6 direct to an api recipe
def recipes_detail(request, recipe_id):
  review_form = ReviewForm
  print(recipe_id)
  recipe_param = {'id': recipe_id}
  api_recipe = accessAPI(get_recipe, recipe_param, 'GET')
  return render(request, 'recipes/detail.html', {
    'recipe': api_recipe,
    'review_form': review_form
  })

def add_review_api(request, recipe_id):

  if not Recipe.objects.get(id=recipe_id):
    params = {'id': recipe_id}
    recipe = accessAPI(recipe_list, params, 'GET')

    external_recipe = Recipe.objects.create(
      recipe_id = external_recipe['id'],
      name = external_recipe['name'],
      description = external_recipe['description'],
      user=User.objects.get(username='llillianlayne')
    )
    add_review_api(request, recipe_id=external_recipe.id)


  form = ReviewForm(request.POST)

  if form.is_valid():
    new_review = form.save(commit=False)
    new_review.recipe_id = recipe.id
    new_review.user = request.user
    new_review.save()
  return redirect('user_recipe', recipe_id=recipe.id)

# 7 authentication
def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('home.html')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

# 8 user creates a recipe
class RecipeCreate(CreateView):
  model = Recipe
  fields = ['name', 'description']

  def form_valid(self, form):
      self.object = form.save()
      return redirect('/recipes')

# 9 user updates a recipe
class RecipeUpdate(UpdateView):
  model = Recipe
  fields = ['name', 'description' ]

  def get_absolute_url(self):
    return self.object.get_absolute_url()

# 10 user deletes a recipe
class RecipeDelete(DeleteView):
   model = Recipe
   sucess_url = '/recipes/'

# 11 user views all the folders they have started
class FolderList(ListView):
  model = Folder

# 12 user creates a folder
class FolderCreate(CreateView):
  model = Folder
  fields = '__all__'
  success_url = '/folders/'

def assoc_folder(request, recipe_id, folder_id):
  Recipe.objects.get(id=recipe_id).folder.add(folder_id)
  return redirect('user_recipe', recipe_id=recipe_id)

class FolderList(ListView):
  model = Folder
  template_name = 'folder_list.html'
  context_object_name = 'folders'

class FolderUpdate(UpdateView):
  model = Folder
  fields = '__all__'

class FolderDelete(DeleteView):
  model = Folder
  success_url = '/folders'

  def delete(self, request, *args, **kwargs):
    self.object = self.get_object()
    # Add any additional deletion logic here if needed
    self.object.delete()
    return redirect(self.get_success_url())

def folders_detail(request, folder_id):
  folder = Folder.objects.get(id=folder_id)
  return render(request, 'appetitApp/folder_detail.html', { 'folder': folder })

# edit review
class ReviewUpdate(UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'appetitApp/edit_reviews.html'  # Your edit review template
    success_url = '/recipes/user/{recipe_id}/' 


def add_photo(request, recipe_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
      s3 = boto3.client('s3')
      # need a unique "key" for S3 / needs image file extension too
      key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
      # just in case something goes wrong
      try:
          bucket = os.environ['S3_BUCKET']
          s3.upload_fileobj(photo_file, bucket, key)
          # build the full url string
          url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
          Photo.objects.create(url=url, recipe_id=recipe_id)
      except Exception as e:
          print('An error occurred uploading file to S3')
          print(e)
      return redirect('user_recipe', recipe_id=recipe_id)
    
