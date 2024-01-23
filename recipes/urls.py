from django.urls import path
from .views import home, RecipeListView, RecipeDetailView, records, about_me, recipes_home


app_name = 'recipes'

urlpatterns = [
    path('', home, name='home'),
    path('recipes_home/', recipes_home, name='recipes_home'),
    path('list/', RecipeListView.as_view(), name="list"),
    path('list/<pk>', RecipeDetailView.as_view(), name='detail'),
    path('records/', records, name='records'),
    path('about_me/', about_me, name='about_me'),
]