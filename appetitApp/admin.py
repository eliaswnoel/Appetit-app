from django.contrib import admin

# Register your models here.
from .models import Recipe
from .models import Ingredients
from .models import Steps
from .models import UserProfile
from .models import Review

admin.site.register(Recipe)
admin.site.register(Review)
admin.site.register(Ingredients)
admin.site.register(Steps)
admin.site.register(UserProfile)