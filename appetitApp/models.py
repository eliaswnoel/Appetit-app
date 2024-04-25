from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


MEASUREMENTS = (
  ('c', 'cups'), 
  ('tbsp', 'tablespoon'), 
  ('tsp', 'teaspoon'), 
  ('oz', 'ounces'), 
  ('fl.oz', 'fluid ounces'), 
  ('lbs', 'pounds'), 
)

class Folder(models.Model):
  name = models.CharField(max_length=50)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('folder_detail', kwargs={'pk': self.id})

class UserProfile(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  folders = models.ManyToManyField(Folder)
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)

  def __str__(self):
    return self.user.username
  
# Recipe main entity
class Recipe(models.Model):
  name = models.CharField(max_length=100)
  description = models.TextField(max_length=300)
  folder = models.ManyToManyField(Folder)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  
  def __str__(self):
    return f'{self.name}({self.id})'
  
  def get_absolute_url(self):
    return reverse('user_recipe', kwargs={'recipe_id': self.id})

class Review(models.Model): 
  text = models.CharField(max_length=300)
  # created_at = models.DateTimeField(auto_now_add=True)
  recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  def __str__(self):
    return f"{self.text}" 

# Ingredients model = foreign key for recipe
class Ingredients(models.Model):
  ingredient = models.CharField(max_length=150)
  recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

  def __str__(self):
    return f'{self.ingredient}'

class Steps(models.Model):
  instructions = models.TextField(max_length=250)
  recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

  def __str__(self):
    return f'{self.instructions}'

class Photo(models.Model):
    url = models.CharField(max_length=200)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for recipe_id: {self.recipe_id} @{self.url}"


  



