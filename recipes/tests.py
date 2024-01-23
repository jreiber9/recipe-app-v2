from django.test import TestCase
from .models import Recipe                   #to access Recipe model
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import RecipeSearchForm
from .views import records

# Create your tests here.

class RecipeModelTest(TestCase):
    #this is the test example
    def setUp(self):
        Recipe.objects.create(
            recipe_id =1,
            name = 'Test recipe',
            cooking_time = 15,
            ingredients = 'ingredient 1, ingredient 2',
            description = 'This is a test recipe.'
        )

    #Here are the tests
        
    def test_recipe_name(self):
        test_recipe = Recipe.objects.get(recipe_id=1)
        field_label = test_recipe._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_description_max_length(self):
        test_recipe = Recipe.objects.get(recipe_id=1)
        max_length = test_recipe._meta.get_field('description').max_length
        self.assertEqual(max_length, 120)

    def test_get_absolute_url(self):
        recipe = Recipe.objects.get(recipe_id=1)
        # get_absolute_url() should take you to the detail page of recipe #1
        # and load the URL /recipe/list/1/
        self.assertEqual(recipe.get_absolute_url(), '/list/1')


class RecipeListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user for login
        User.objects.create_user(username='testuser', password='testpass')

    def test_recipe_list_view_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('recipes:list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/list/')

    def test_recipe_list_view_loads_if_logged_in(self):
        # Log in the user
        self.client.login(username='testuser', password='testpass')

        response = self.client.get(reverse('recipes:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/all_recipes.html')


class RecipeSearchFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user for login
        cls.user = User.objects.create_user(username='testuser', password='testpass')

        # Create test recipes for searching
        cls.recipe1 = Recipe.objects.create(
            name='Test Recipe 1',
            cooking_time=20,
            ingredients='Ingredient 1, Ingredient 2',
            description='This is a test recipe 1.'
        )
        cls.recipe2 = Recipe.objects.create(
            name='Test Recipe 2',
            cooking_time=30,
            ingredients='Ingredient 3, Ingredient 4',
            description='This is a test recipe 2.'
        )

    def test_search_form(self):
        # Log in the test user
        self.client.login(username='testuser', password='testpass')

        # Perform a search using the form
        response = self.client.post(reverse('recipes:records'), {'recipe_title': 'Test Recipe 1'})

        # Check if the search result contains the expected recipe
        self.assertContains(response, 'Test Recipe 1')
        self.assertNotContains(response, 'Test Recipe 2')


class RecipeModelAdditionalTest(TestCase):
    def setUp(self):
        Recipe.objects.create(
            recipe_id=2,
            name='Another Test Recipe',
            cooking_time=25,
            ingredients='ingredient 3, ingredient 4',
            description='This is another test recipe.'
        )

    def test_recipe_cooking_time(self):
        test_recipe = Recipe.objects.get(recipe_id=2)
        self.assertEqual(test_recipe.cooking_time, 25)


class RecipeSearchFormTest(TestCase):
    def test_recipe_search_form_valid_data(self):
        form_data = {'recipe_title': 'Test Recipe', 'chart_type': '#1'}
        form = RecipeSearchForm(data=form_data)

        # Check if the form is valid
        self.assertTrue(form.is_valid())

class RecipeRecordsViewTest(TestCase):
    def setUp(self):
        # Create a user for login
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_records_view_loads(self):
        # Log in the test user
        self.client.login(username='testuser', password='testpass')

        # Send a GET request to the records view
        response = self.client.get('/records/')

        # Check if the view returns a successful status code (200)
        self.assertEqual(response.status_code, 200)

        # Check if the 'records.html' template is used in the response
        self.assertTemplateUsed(response, 'recipes/records.html')