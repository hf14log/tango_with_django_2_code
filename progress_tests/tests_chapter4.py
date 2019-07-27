# 
# Tango with Django 2 Progress Tests
# By Leif Azzopardi and David Maxwell
# With assistance from Enzo Roiz (https://github.com/enzoroiz)
# 
# Chapter 4 -- Templates and Media Files
# 

#
# In order to run these tests, copy this module to your tango_with_django_project/rango/ directory.
# Once this is complete, run $ python manage.py test rango.tests_chapter4
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

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

class Chapter4ProjectStructureTests(TestCase):
    """
    Have you set templates, static files and media files up correctly, as per the book?
    """
    def setUp(self):
        self.project_base_dir = os.getcwd()
        self.templates_dir = os.path.join(self.project_base_dir, 'templates')
        self.rango_templates_dir = os.path.join(self.templates_dir, 'rango')
    
    def test_templates_directory_exists(self):
        """
        Does the templates/ directory exist?
        """
        directory_exists = os.path.isdir(self.templates_dir)
        self.assertTrue(directory_exists, f"{FAILURE_HEADER}Your project's templates directory does not exist.{FAILURE_FOOTER}")
    
    def test_rango_templates_directory_exists(self):
        """
        Does the templates/rango/ directory exist?
        """
        directory_exists = os.path.isdir(self.rango_templates_dir)
        self.assertTrue(directory_exists, f"{FAILURE_HEADER}The Rango templates directory does not exist.{FAILURE_FOOTER}")
    
    def test_template_dir_setting(self):
        """
        Does the TEMPLATE_DIR setting exist, and does it point to the right directory?
        """
        variable_exists = 'TEMPLATE_DIR' in dir(settings)
        self.assertTrue(variable_exists, f"{FAILURE_HEADER}Your settings.py module does not have the variable TEMPLATE_DIR defined!{FAILURE_FOOTER}")
        
        template_dir_value = os.path.normpath(settings.TEMPLATE_DIR)
        template_dir_computed = os.path.normpath(self.templates_dir)
        self.assertTrue(template_dir_value, template_dir_computed, f"{FAILURE_HEADER}Your TEMPLATE_DIR setting does not point to the expected path. Check your configuration, and try again.{FAILURE_FOOTER}")
    
    def test_template_lookup_path(self):
        """
        Does the TEMPLATE_DIR value appear within the lookup paths for templates?
        """
        lookup_list = settings.TEMPLATES[0]['DIRS']
        found_path = False
        
        for entry in lookup_list:
            entry_normalised = os.path.normpath(entry)
            
            if entry_normalised == os.path.normpath(settings.TEMPLATE_DIR):
                found_path = True
        
        self.assertTrue(found_path, f"{FAILURE_HEADER}Your project's templates directory is not listed in the TEMPLATES>DIRS lookup list. Check your settings.py module.{FAILURE_FOOTER}")
    
    def test_templates_exist(self):
        """
        Do the index.html and about.html templates exist in the correct place?
        """
        index_path = os.path.join(self.rango_templates_dir, 'index.html')
        about_path = os.path.join(self.rango_templates_dir, 'about.html')
        
        self.assertTrue(os.path.isfile(index_path), f"{FAILURE_HEADER}Your index.html template does not exist, or is in the wrong location.{FAILURE_FOOTER}")
        self.assertTrue(os.path.isfile(about_path), f"{FAILURE_HEADER}Your about.html template does not exist, or is in the wrong location.{FAILURE_FOOTER}")


class Chapter4IndexPageTests(TestCase):
    """
    A series of tests to ensure that the index page/view has been updated to work with templates.
    Image tests are in the Chapter4StaticMediaTests suite.
    """
    def setUp(self):
        self.response = self.client.get(reverse('index'))
    
    def test_index_uses_template(self):
        """
        Checks whether the index view uses a template -- and the correct one!
        """
        self.assertTemplateUsed(self.response, 'rango/index.html', f"{FAILURE_HEADER}Your index() view does not use the expected index.html template.{FAILURE_FOOTER}")
    
    def test_index_uses_context_dictionary(self):
        """
        Tests whether the index view uses the context dictionary correctly.
        Crunchy, creamy cookie, anyone?
        """
        self.assertTrue('boldmessage' in self.response.context, f"{FAILURE_HEADER}In your index view, the context dictionary is not passing the boldmessage key. Check your context dictionary in the index() view, located in rango/views.py, and try again.{FAILURE_FOOTER}")
        
        message = self.response.context['boldmessage']
        expected = 'Crunchy, creamy, cookie, candy, cupcake!'
        self.assertEqual(message, expected,  f"{FAILURE_HEADER}The boldmessage being sent to the index.html template does not match what is expected. Check your index() view. Make sure you match up cases, and don't miss any punctuation! Even one missing character will cause the test to fail.{FAILURE_FOOTER}")
    
    def test_index_starts_with_doctype(self):
        """
        Is the <!DOCTYPE html> declaration on the first line of the index.html template?
        """
        self.assertTrue(self.response.content.decode().startswith('<!DOCTYPE html>'), f"{FAILURE_HEADER}Your index.html template does not start with <!DOCTYPE html> -- this is requirement of the HTML specification.{FAILURE_FOOTER}")
    
    def test_about_link_present(self):
        """
        Is the about hyperlink present and correct on the index.html template?
        """
        expected = "<a href=\"/rango/about/\">About</a><br />"
        self.assertTrue(expected in self.response.content.decode(), f"{FAILURE_HEADER}Your index.html template doesn't contain the /rango/about/ link -- or it is not correct. Make sure you have the linebreak in, too!{FAILURE_FOOTER}")
        

class Chapter4StaticMediaTests(TestCase):
    """
    A series of tests to check whether static files and media files have been setup and used correctly.
    Also tests for the two required files -- rango.jpg and cat.jpg.
    """
    pass


class Chapter4ExerciseTests(TestCase):
    """
    A series of tests to ensure that the exercise listing at the end of Chapter 4 has been completed.
    """
    pass