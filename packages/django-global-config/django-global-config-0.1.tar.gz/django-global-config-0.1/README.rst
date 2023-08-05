=====
Global Config
=====

Quick start
-------------------------

1. Install using pip::

    pip install django-global-config

2. Add "global_config" to your INSTALLED_APPS setting like this (it should be last!)::

    INSTALLED_APPS = [
        ...
        'global_config',
    ]

3. Creating a new file to hold your config::

    mkdir [PROJECT_ROOT]/[PROJECT_NAME]/config.py

4. Create a class within config.py with your keys and default values::

    from global_config import GlobalConfig

    class Config(GlobalConfig):
        MY_CONFIG_KEY1 = 'this is a default value, but if you add a new ConfigItem in the admin it will update dynamically!'
        MY_CONFIG_KEY2 = 123
        MY_CONFIG_KEY3 = ['a', 'b', 'c']
        MY_CONFIG_KEY4 = 12.0
        MY_CONFIG_KEY5 = True

5. Reference your config as if it were a vanilla python class::

    from django.http import HttpResponse
    from [PROJECT_NAME].config import Config

    def my_view(request):
        return HttpResponse('My dynamic value for "MY_CONFIG_KEY1": ' + Config.MY_CONFIG_KEY1)
