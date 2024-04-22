from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Recipe
from .forms import ReviewForm, IngredientForm, StepsForm
from .api_manage import accessAPI

recipe_list = '/recipes/list/'
tags_list = '/tags/list/'
get_recipe = '/recipes/get-more-info/'


# homepage view
def home(request): 
  # get most popular recipes
  popular_params = {'from': '0', 'size':4,'q':'feature_page',"sort":"approved_at:desc"}
  popular_recipes = accessAPI(recipe_list, popular_params, 'GET')
  popular_recipes_data = popular_recipes['results']
  user_recipes = Recipe.objects.all()
  # get cuisine types 
  cuisine_tags = accessAPI(tags_list, '', 'GET')
  cuisine_tags_data = cuisine_tags['results']
  return render(request, 'home.html', {
    'popular_recipes': popular_recipes_data,
    'cuisines': cuisine_tags_data,
    'user_recipes': user_recipes,
  })

def recipes_index(request):
  recipes = Recipe.objects.all()
  return render(request, 'recipes/index.html', {
    'recipes': recipes
  })

# direct to a user created recipe
def recipes_user_recipe(request, recipe_id):
  recipes = Recipe.objects.get(id=recipe_id)
  ingredient_form = IngredientForm
  steps_form = StepsForm
  print()
  return render(request, 'recipes/user/user_recipe.html', {
    'recipe': recipes, 
    'ingredient_form': ingredient_form, 
    'steps_form': steps_form
  })

def add_ingredient(request, recipe_id):
  form = IngredientForm(request.POST)

  if form.is_valid():
    new_ingredient = form.save(commit=False)
    new_ingredient.recipe_id = recipe_id
    new_ingredient.save()
  return redirect('user_recipe', recipe_id=recipe_id)

# add steps
def add_steps(request, recipe_id):
  form = StepsForm(request.POST)

  if form.is_valid():
    new_step = form.save(commit=False)
    new_step.recipe_id = recipe_id
    new_step.save()
  return redirect('user_recipe', recipe_id=recipe_id)
# direct to an api recipe
def recipes_detail(request, recipe_id):
  recipe_param = {'id': str(recipe_id)}
  api_recipe = accessAPI(get_recipe, recipe_param, 'GET')
  return render(request, 'recipes/detail.html', {
    'api_recipe': api_recipe,
  })

# authentication
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

class RecipeCreate(CreateView):
  model = Recipe
  fields = '__all__'

  def form_valid(self, form):
      self.object = form.save()
      return redirect('/recipes')




# def add_review(request, recipe_id):
#     recipe = Recipe.objects.get(pk=recipe_id)
#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.recipe = recipe
#             review.save()
#             return redirect('recipe_detail', recipe_id=recipe_id)
#     else:
#         form = ReviewForm()
#     return render(request, 'review_form.html', {'form': form, 'recipe': recipe})

    # recipe = Recipe.objects.get(id=recipe_id)
    # if request.method == 'POST':
    #     form = ReviewForm(request.POST)
    #     if form.is_valid():
    #         review = form.save(commit=False)
    #         review.user = request.user
    #         review.recipe = recipe
    #         review.save()
    #         return redirect('recipe_detail', recipe_id=recipe.id)
    # else:
    #     form = ReviewForm()
    # return render(request, 'recipes/detail.html', {'recipe': recipe, 'form': form})


