from django.forms import ModelForm
from .models import Recipe, Ingredients, ReviewModel, Steps

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
        model = ReviewModel
        fields = ['text']
        
class StepsForm(ModelForm):
    class Meta:
        model = Steps
        fields = ['instructions']

