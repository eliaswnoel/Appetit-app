from django.forms import ModelForm
from .models import Recipe, Ingredients, Review, Steps, Folder
from django import forms

class RecipeForm(ModelForm):
    class Meta: 
        model = Recipe
        fields =['name', 'description']
 
class IngredientForm(ModelForm):
    class Meta: 
        model = Ingredients
        fields = ['ingredient']

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['text']

        
class StepsForm(ModelForm):
    class Meta:
        model = Steps
        fields = ['instructions']


class FolderForm(ModelForm):
    class Meta:
        model = Folder
        fields = ['name']