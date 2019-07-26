# 
# Tango with Django 2 Progress Tests
# By Leif Azzopardi and David Maxwell
# With assistance from Enzo Roiz (https://github.com/enzoroiz)
# 
# Chapter 3 -- Django Basics
# 

#
# In order to run these tests, copy this module to your tango_with_django_project/rango/ directory.
# Once this is complete, run $ python manage.py test rango.tests_chapter3
# 
# The tests will then be run, and the output displayed -- do you pass them all?
# 
# Once you are done with the tests, delete the module. You don't need to put it in your Git repository!
#

import os
import importlib
from django.urls import reverse
from django.test import TestCase
from django.conf import settings

class Chapter3ProjectStructureTests(TestCase):
    """
    Simple tests to probe the file structure of your project so far.
    We also include a test to check whether you have added rango to your list of INSTALLED_APPS.
    """
    def setUp(self):
        self.project_base_dir = os.getcwd()
        self.rango_app_dir = os.path.join(self.project_base_dir, 'rango')
    
    def test_project_created(self):
        """
        Tests whether the tango_with_django_project configuration directory is present and correct.
        """
        directory_exists = os.path.isdir(os.path.join(self.project_base_dir, 'tango_with_django_project'))
        urls_module_exists = os.path.isfile(os.path.join(self.project_base_dir, 'tango_with_django_project', 'urls.py'))
        
        self.assertTrue(directory_exists)
        self.assertTrue(urls_module_exists)
    
    def test_rango_app_created(self):
        """
        Determines whether the Rango app has been created.
        """
        directory_exists = os.path.isdir(self.rango_app_dir)
        is_python_package = os.path.isfile(os.path.join(self.rango_app_dir, '__init__.py'))
        views_module_exists = os.path.isfile(os.path.join(self.rango_app_dir, 'views.py'))
        
        self.assertTrue(directory_exists)
        self.assertTrue(is_python_package)
        self.assertTrue(views_module_exists)
    
    def test_rango_has_urls_module(self):
        """
        Did you create a separate urls.py module for Rango?
        """
        module_exists = os.path.isfile(os.path.join(self.rango_app_dir, 'urls.py'))
        
        self.assertTrue(module_exists)
    
    def test_is_rango_app_configured(self):
        """
        Did you add the new Rango app to your INSTALLED_APPS list?
        """
        is_app_configured = 'rango' in settings.INSTALLED_APPS
        
        self.assertTrue(is_app_configured)
    
class Chapter3IndexPageTests(TestCase):
    """
    Testing the basics of your index view and URL mapping.
    Also runs tests to check the response from the server.
    """
    def setUp(self):
        self.views_module = importlib.import_module('rango.views')
        self.views_module_listing = dir(self.views_module)
        
        self.project_urls_module = importlib.import_module('tango_with_django_project.urls')
    
    def tearDown(self):
        pass
    
    def test_view_exists(self):
        """
        Does the index() view exist in Rango's views.py module?
        """
        name_exists = 'index' in self.views_module_listing
        is_callable = callable(self.views_module.index)
        
        self.assertTrue(name_exists)
        self.assertTrue(is_callable)
    
    def test_mappings_exists(self):
        """
        Are the two required URL mappings present and correct?
        One should be in the project's urls.py, the second in Rango's urls.py.
        We have the 'index' view named twice -- it should resolve to '/rango/'.
        """
        index_mapping_exists = False
        
        # This is overridden. We need to manually check it exists.
        for mapping in self.project_urls_module.urlpatterns:
            if hasattr(mapping, 'name'):
                if mapping.name == 'index':
                    index_mapping_exists = True
        
        self.assertTrue(index_mapping_exists)
        self.assertEquals(reverse('index'), '/rango/')
    
    def test_response(self):
        """
        Does the response from the server contain the required string?
        """
        response = self.client.get(reverse('index'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rango says hey there partner!")
    
    def test_for_about_hyperlink(self):
        """
        Does the response contain the about hyperlink required in the exercise?
        Checks for both single and double quotes in the attribute. Both are acceptable.
        """
        response = self.client.get(reverse('index'))
        
        single_quotes_check = '<a href=\'/rango/about/\'>About</a>' in response.content.decode()
        double_quotes_check = '<a href="/rango/about/">About</a>' in response.content.decode()
        
        self.assertTrue(single_quotes_check or double_quotes_check)

class Chapter3AboutPageTests(TestCase):
    """
    Tests to check the about view.
    We check whether the view exists, the mapping is correct, and the response is correct.
    """
    def setUp(self):
        self.views_module = importlib.import_module('rango.views')
        self.views_module_listing = dir(self.views_module)
    
    def test_view_exists(self):
        """
        Does the about() view exist in Rango's views.py module?
        """
        name_exists = 'about' in self.views_module_listing
        is_callable = callable(self.views_module.about)
        
        self.assertTrue(name_exists)
        self.assertTrue(is_callable)
    
    def test_mapping_exists(self):
        """
        Checks whether the about view has the correct URL mapping.
        """
        self.assertEquals(reverse('about'), '/rango/about/')
    
    def test_response(self):
        """
        Checks whether the view returns the required string to the client.
        """
        response = self.client.get(reverse('about'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rango says here is the about page.")
    
    def test_for_index_hyperlink(self):
        """
        Does the response contain the index hyperlink required in the exercise?
        Checks for both single and double quotes in the attribute. Both are acceptable.
        """
        response = self.client.get(reverse('about'))
        
        single_quotes_check = '<a href=\'/rango/\'>Index</a>' in response.content.decode()
        double_quotes_check = '<a href="/rango/">Index</a>' in response.content.decode()
        
        self.assertTrue(single_quotes_check or double_quotes_check)