=========
djcorecap
=========

Core app for Django projects that provides essential functions, tags, and
enhanced Bootstrap-friendly templates.

* Free software: MIT license


Features
--------

* Custom base template that plays nicely with Bootstrap (and themes)
* Custom allauth templates that play nicely with Bootstrap (and themes)
* Paginator template snippet ready for inclusion in other templates
* Convenience functions to support Bokeh plots
* Template tags for auto-setting links to active and formatting percentages
* Bootstrap test page


Installation
------------

Add djcorecap to your INSTALLED_APPS in settings.
Ensure that it comes before all other third party apps to enable 
template overrides, etc.  

If you plan to use the app's base template 
as your project's base template, replace base.html in 
project/templates/ with a file containing the following:

.. code-block:: jinja

   {% extends 'djcorecap/base.html' %}

If you plan to use djcorecap's version of the allauth templates, delete 
the account/ folder (if exists) from project/templates/.
