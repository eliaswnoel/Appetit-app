from django.forms import ModelForm
from .models import Recipe, Ingredients, Review, Steps

class RecipeForm(ModelForm):
    class Meta: 
        model = Recipe
        fields =['name', 'description']

class IngredientForm(ModelForm):
    class Meta: 
        model = Ingredients
        fields = ['ingredient', 'measurement', 'amount']

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['text']
        
class StepsForm(ModelForm):
    class Meta:
        model = Steps
        fields = ['instructions']

