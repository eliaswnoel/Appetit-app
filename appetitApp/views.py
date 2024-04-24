import uuid
import os
import boto3
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Recipe, Folder, Review, Photo
from .forms import ReviewForm, IngredientForm, StepsForm
from .api_manage import accessAPI
from django.urls import reverse_lazy

recipe_list = '/recipes/list'
tags_list = '/tags/list'
get_recipe = '/recipes/get-more-info'

# homepage view
def home(request): 
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
def recipes_index(request):
  recipes = Recipe.objects.all()
  return render(request, 'recipes/index.html', {
    'recipes': recipes
  })

# 2 direct to a user created recipe
def recipes_user_recipe(request, recipe_id):
  recipe = Recipe.objects.get(id=recipe_id)
  ingredient_form = IngredientForm
  steps_form = StepsForm
  review_form = ReviewForm
    
  return render(request, 'recipes/user/user_recipe.html', {
    'recipe': recipe, 
    'ingredient_form': ingredient_form, 
    'steps_form': steps_form, 
    'review_form': review_form
  })

# 3 add review to recipe
def add_review(request, recipe_id):
  form = ReviewForm(request.POST)

  if form.is_valid():
    new_review = form.save(commit=False)
    new_review.recipe_id = recipe_id
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
  print(recipe_id)
  recipe_param = {'id': recipe_id}
  api_recipe = accessAPI(get_recipe, recipe_param, 'GET')
  return render(request, 'recipes/detail.html', {
    'recipe': api_recipe,
  })

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
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

# 8 user creates a recipe
class RecipeCreate(CreateView):
  model = Recipe
  fields = '__all__'

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
   sucess_url = '/recipes'

# 11 user views all the folders they have started
class FolderList(ListView):
  model = Folder

# 12 user creates a folder
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
          # we can assign to cat_id or cat (if you have a cat object)
          Photo.objects.create(url=url, cat_id=recipe_id)
      except Exception as e:
          print('An error occurred uploading file to S3')
          print(e)
      return redirect('user_recipe', recipe_id=recipe_id)
    
