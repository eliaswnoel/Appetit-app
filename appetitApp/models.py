from django.db import models
from django.contrib.auth.models import User

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
  description = models.CharField(max_length=300)


  def __str__(self):
    return f'{self.name}({self.id})'


# Directions model = foreign key for recipe
class directions(models.Model):
  description = models.CharField(max_length=400)


  def __str__(self):
    return f'{self.description}'


# Ingredients model = foreign key for recipe
class Ingredients(models.Model):
  ingredient = models.CharField(max_length=150)
  measurement = models.CharField(
    max_length=100, 
    choices=MEASUREMENTS,
    default=MEASUREMENTS[0][0]
  )
  amount = models.IntegerField()

  recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

  def __str__(self):
    return f'{self.ingredient}'
  

class UseProfile(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.user.username

