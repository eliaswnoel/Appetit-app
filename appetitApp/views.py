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
from .models import Recipe, Folder, Review, Photo, UserProfile
from .forms import ReviewForm, IngredientForm, StepsForm, UserProfileForm
from .api_manage import accessAPI, fetch_recipe_from_api
from django.urls import reverse
from django.conf import settings

recipe_list = '/recipes/list'
tags_list = '/tags/list'
get_recipe = '/recipes/get-more-info'

# startup --------------------
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

  user_data = Recipe.objects.filter(user=request.user)
  return render(request, 'home.html', {
    'popular_recipes': popular_json,
    'cuisines': cuisine_tags_json,
    'user_recipes': user_recipes,
    'tags': tags_display, 
    'user_data': user_data
  })

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


# recipe views for user based recipes
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

def add_review(request, recipe_id):
  form = ReviewForm(request.POST)

  if form.is_valid():
    new_review = form.save(commit=False)
    new_review.recipe_id = recipe_id
    new_review.user = request.user
    new_review.save()
  return redirect('user_recipe', recipe_id=recipe_id)

class ReviewDelete(DeleteView):
  model = Review
  success_url = '/recipes/user/{recipe_id}/'

  def delete(self, request, *args, **kwargs):
    self.object = self.get_object()
    self.object.delete()
    return redirect(self.get_success_url())


def add_ingredient(request, recipe_id):
  form = IngredientForm(request.POST)

  if form.is_valid():
    new_ingredient = form.save(commit=False)
    new_ingredient.recipe_id = recipe_id
    new_ingredient.save()
  return redirect('user_recipe', recipe_id=recipe_id)

def add_steps(request, recipe_id):
  form = StepsForm(request.POST)

  if form.is_valid():
    new_step = form.save(commit=False)
    new_step.recipe_id = recipe_id
    new_step.save()
  return redirect('user_recipe', recipe_id=recipe_id)

def recipes_detail(request, recipe_id):
  review_form = ReviewForm
  print(recipe_id)
  recipe_param = {'id': recipe_id}
  api_recipe = accessAPI(get_recipe, recipe_param, 'GET')
  return render(request, 'recipes/detail.html', {
    'recipe': api_recipe,
    'review_form': review_form
  })


# CRUD recipes
class RecipeCreate(CreateView):
  model = Recipe
  fields = ['name', 'description']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)
    
  # def get_success_url(self):   
  #     return reverse('user_recipe', kwargs={'pk': self.object.pk})

class RecipeUpdate(UpdateView):
  model = Recipe
  fields = ['name', 'description' ]

  def get_absolute_url(self):
    return self.object.get_absolute_url()

class RecipeDelete(DeleteView):
  model = Recipe
  sucess_url = '/home'
  def get_success_url(self):
    return reverse('home')

class ReviewUpdate(UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'appetitApp/edit_reviews.html' 
    success_url = '/recipes/user/{recipe_id}/' 

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

def create_user_profile(request):
  form = UserProfileForm.POST
  if form.is_valid():
    new = form.save(commit=False)
    new.user = request.user
    new.save()
  return redirect('home')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('home.html')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)


# CRUD Folders
class FolderCreate(CreateView):
  model = Folder
  fields = '__all__'
  success_url = '/folders/'

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
    self.object.delete()
    return redirect(self.get_success_url())

def assoc_folder(request, recipe_id, folder_id):
  Recipe.objects.get(id=recipe_id).folder.add(folder_id)
  return redirect('user_recipe', recipe_id=recipe_id)

def folders_detail(request, folder_id):
  recipes = Recipe.objects.all()
  folder = Folder.objects.get(id=folder_id)
  id_list = recipes.folder.all().valuse_list('id')
  exclude_recipes = Recipe.objects.exclude(id__in=id_list)
  return render(request, 'appetitApp/folder_detail.html', { 'folder': folder, 'recipes': exclude_recipes })

def add_photo(request, recipe_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
      s3 = boto3.client('s3')
      key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
      try:
          bucket = os.environ['S3_BUCKET']
          s3.upload_fileobj(photo_file, bucket, key)
          url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
          Photo.objects.create(url=url, recipe_id=recipe_id)
      except Exception as e:
          print('An error occurred uploading file to S3')
          print(e)
      return redirect('user_recipe', recipe_id=recipe_id)
    
