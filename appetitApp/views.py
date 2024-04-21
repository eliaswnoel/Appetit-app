from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Recipe
from .api_manage import getPopularRecipes

# homepage view
def home(request): 
  popular_recipes = getPopularRecipes(4)
  popular_recipes_data = popular_recipes['results']
  return render(request, 'home.html', {
    'popular_recipes': popular_recipes_data
  })


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
      return redirect('home')



def recipes_detail(request, recipe_id):
  recipe = Recipe.objects.get(id=recipe_id)
  return render(request, 'recipes/detail.html', { 'recipe': recipe })


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