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
 

# Recipe main entity
class Recipe(models.Model):
  name = models.CharField(max_length=100)
  description = models.TextField(max_length=300)

  def __str__(self):
    return f'{self.name}({self.id})'
  
  def get_absolute_url(self):
    return reverse('detail', kwargs={'recipe_id': self.id})


   

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


class Review(models.Model):
  text = models.TextField(max_length=300)
  recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.text}" 


class UserProfile(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.user.username
  

class Folder(models.Model):
  name = models.CharField(max_length=50)

  def __str__(self):
    return self.name



class ReviewModel(models.Model):
  text = models.TextField(max_length=300)
  recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.text}" 

class ReviewModel(models.Model):
  text = models.TextField(max_length=300)
  recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.text}" 

  



