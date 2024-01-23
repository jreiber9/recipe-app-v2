from django.shortcuts import render
from django.views.generic import ListView, DetailView   #to display lists
from .models import Recipe                #to access Recipe model
#to protect class-based view
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RecipeSearchForm
# from .utils import get_recipename_from_id, get_chart
import pandas as pd

# Create your views here.
def home(request):
    return render(request, 'recipes/recipes_home.html')

def recipes_home(request):
    return render(request, 'recipes/recipes_home.html')

#about me page
def about_me(request):
    return render(request, 'recipes/about_me.html')

class RecipeListView(LoginRequiredMixin, ListView):           #class-based view
   model = Recipe                         #specify model
   template_name = 'recipes/all_recipes.html'    #specify template 

class RecipeDetailView(LoginRequiredMixin, DetailView):                       #class-based view
   model = Recipe                                       #specify model
   template_name = 'recipes/detail.html'                 #specify template

def records(request):
    # create an instance of RecipeSearchForm that you defined in recipes/forms.py
    form = RecipeSearchForm(request.POST or None)
    recipes = None  # initialize recipes queryset to None

    # check if the button is clicked
    if request.method == 'POST':
        # read recipe_title
        recipe_title = request.POST.get('recipe_title')

        # retrieve all recipes without applying any filter
        all_recipes = Recipe.objects.all()

        if all_recipes.exists():  # if any recipes found
            # Apply filter based on the entered recipe title
            recipes = all_recipes.filter(name__icontains=recipe_title)

    # pack up data to be sent to the template in the context dictionary
    context = {
        'form': form,
        'recipes': recipes,
    }

    # load the recipes/records.html page using the data that you just prepared
    return render(request, 'recipes/records.html', context)
