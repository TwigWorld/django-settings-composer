# django-settings-composer
A 'sensible' way to gather settings dynamically.

## Rationale

Django allows developers to reference only a single settings file, and leaves it entirely up to the developers to contrive a way to make their settings dynamic based on environmental or other settings.

> We don't need a default solution for this. It's not within the scope of this project to tell people how they should organize their settings files. Take that opportunity to showcase your individualism." <cite>Adrian Holovaty, Django co-creator</cite>

That's all very well, and unique development environments often require bespoke solutions, but most of us are trying to solve the same problem without any accepted pattern to do so. The result can be complex and hard to follow settings files, with duplicated definitions and multiple chains of inheritence.

Django Settings Composer seeks to provide:

- minimal setup
- maximum flexibility
- ability to use the exact same syntax as standard Django settings files (no class definiitons)
- clear, consistent update/override rules
- introspection to see exactly how a given Django Settings object was compiled

Django Settings Composer allows you to:

1. define project wide global settings and defaults
2. suplement or override these with site-specific settings
3. define environment-specific settings such as databases and keys
4. switch on/off whole setting groups, such as debug mode or https
5. exclude certain apps, middleware etc. under certain conditions

## Setup

You can use as much or as little of the customisablity as you require. Django Settings Composer merely provides a basic framework and a few conventions to follow. The setting loader logic will look for files based on a particular permutation of environmental variables. If certain environmental variables are not set, Django Settings Composer will not attempt to load settings for them.

The loading logic is as follows:

1. A project-wide settings module
2. A project-wide, environment-specific settings module
3. A site-specific settings module
4. A site-specific, environment-specific settings module

### Environment variables

Firstly, point Django to the settings composer settings file.

```
export DJANGO_SETTINGS_MODULE=settings_composer.settings
```

Then you only really need to set one other environment variable to get going:

**SETTINGS_COMPOSER_MODULE**

This is the python module that contains your settings within your project. It is effectively a replacement for **DJANGO_SETTINGS_MODULE**.

```
export SETTINGS_COMPOSER_MODULE=myproject.settings
```

You may also set:

**SETTINGS_COMPOSER_SITE**

This is the python module within _myproject.settings.sites_ that contains the site settings files.

```
export SETTINGS_COMPOSER_SITE=mysite
```

**SETTINGS_COMPOSER_ENV**

This is the settings file within _myproject.settings.env_ and/or _myproject.settings.sites.mysite.env_ that contains environment/site-environment specific settings.

```
export SETTINGS_COMPOSER_ENV=staging
```

**SETTINGS_COMPOSER_SWITCHES**

This is a comma separated list of switches in the form (group_name):(switch_name). These switches will be applied immediately after all the modules have been loaded. They must have been defined somewhere in the loaded settings (see **Advanced Usage**).

```
export SETTINGS_COMPOSER_SWITCHES=debug:off,database:test
```

**SETTINGS_COMPOSER_VERBOSE**

If set to 'true' or 'yes', Django Settings Composer will report each step it takes throughout the loading phase.

```
export SETTINGS_COMPOSER_VERBOSE=yes
```

### Example project layout with multiple environments

```
export SETTINGS_COMPOSER_MODULE=myproject.settings
export SETTINGS_COMPOSER_ENV=production
```

```
manage.py
    myproject/
        __init__.py
        urls.py
        wsgi.py
        settings/
            __init__.py
            env/
                __init__.py
                local.py
                production.py
```

This will load the following settings modules:

```
myproject.settings
myproject.settings.env.production
```

### Example project layout with multiple sites

```
export SETTINGS_COMPOSER_MODULE=myproject.settings
export SETTINGS_COMPOSER_SITE=site_1
```

```
manage.py
    myproject/
        __init__.py
        urls.py
        wsgi.py
        settings/
            __init__.py
            env/
                __init__.py
                local.py
                production.py
            sites/
                __init__.py
                site_1.py
                site_2.py
```

This will load the following settings modules:

```
myproject.settings
myproject.settings.sites.site_1
```

### Example project layout with multiple sites and environments

```
export SETTINGS_COMPOSER_MODULE=myproject.settings
export SETTINGS_COMPOSER_SITE=site_2
export SETTINGS_COMPOSER_ENV=staging
```

```
manage.py
    myproject/
        __init__.py
        urls.py
        wsgi.py
        settings/
            __init__.py
            env/
                __init__.py
                local.py
                staging.py
                production.py
            sites/
                __init__.py
                site_1/
                    __init__.py
                    env/
                        __init__.py
                        local.py
                        staging.py
                        production.py
                site_2/
                    __init__.py
                    env/
                        __init__.py
                        local.py
                        staging.py
                        production.py
```

This will load the following settings modules:

```
myproject.settings
myproject.settings.env.staging
myproject.settings.sites.site_2
myproject.settings.sites.site_2.env.staging
```

## Basic usage

In the simplest case, just create the settings files you need and define settings in them just as you would a normal Django settings file.

There is no inheritence to work out, just a fixed loading order.

Each settings file is self contained, so for example using the above setup you can't _directly_ access settings defined in 'myproject.settings.env.staging' within 'myproject.settings.sites.site_2.env.staging' (but you can still overwrite previously defined settings).

If more fluidity is required, Django Settings Composer provides a range of definable 'actions' that can be triggered when a settings module is loaded.

## Advanced usage

It is very much by design that individal settings files aren't aware of other settings files. This is in order to minimise the complication of inheritence.

With that said, there are certain situations where you want to adjust a previously defined setting without redefining it, or access the current settings context.

The following actions can be included in a settings module to trigger advanced behaviours.

_Note: When a module is loaded, actions are executed in the following order, before the module's settings are applied. The exception is on_complete actions, which are executed after all the main modules have been loaded and applied._

### load

Simply loads the named module or modules. This happens ahead of any other actions.

The main reason for using this rather than importing the module via Python imports is that Django Settings Composer tracks the import for debugging purposes.

```
import settings_composer

settings_composer.load(
    'settings.definitions',
    'settings.globals',
    'settings.defaults',
    'settings.on_complete'
)

```

### create_switch

Defines a switch, which consists of a group and switch name, as either a settings dictionary, or a module path.

```
import settings_composer

settings_composer.create_switch('debug', 'off', {
    'DEBUG': False,
    'TEMPLATE_DEBUG': False,
    'DEBUG_PROPAGATE_EXCEPTIONS': False
})
settings_composer.create_switch('debug', 'on', {
    'DEBUG': True,
    'TEMPLATE_DEBUG': True,
    'DEBUG_PROPAGATE_EXCEPTIONS': False
})
settings_composer.create_switch('debug', 'propagate', {
    'DEBUG': True,
    'TEMPLATE_DEBUG': True,
    'DEBUG_PROPAGATE_EXCEPTIONS': True
})

settings_composer.create_switch('https', 'off', 'settings.switches.https_off')
settings_composer.create_switch('https', 'on', 'settings.switches.https_on')

```

### apply_switch

Apply a previously defined switch.

```
import settings_composer

settings_composer.apply_switch('debug', 'off')
settings_composer.apply_switch('https', 'on')
```

### set

Set the named setting(s) directly. In general you can simply create the definiton as a module assignment, but this is still useful for defining settings within a function or if you need to set values before other actions are executed.

```
import settings_composer

settings_composer.set(FOO=True, BAR=False)

# is the same as

FOO = True
BAR = False
```

### extend_setting

Extend a previously defined list setting with another list.

```
import settings_composer

settings_composer.extend_setting(INSTALLED_APPS, ['debug_tools', 'testing_tools'])
```


### update_setting

Update a previously defined dictionary setting with new values.

```
import settings_composer

settings_composer.update_setting(
    DATABASES,
    default={
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test',
    }
)
```


### exclude_from_setting

Exclude values from a previously defined setting. This can either be items from a list or keys from a dictionary.

```
settings_composer.exclude_from_setting('INSTALLED_APPS', ['debug_tools', 'testing_tools'])
settings_composer.exclude_from_setting('DATABASES', ['backup'])
```

### on_complete

To use this action, pass in a function. The function should take a single argument, which is a dictionary of all the current settings.

This provides a fairly reliable way of accessing, checking and updating previously defined settings once they have been loaded into a complete state.

Be wary of modifying the settings dictionary directly - Django Settings Composer has no visibility of these changes so it will make debugging more difficult.

_Note: You can trigger actions from within the function, including other on_complete actions, but it would be best practice to keep the logic within the function simple._

```
import settings_composer

def cleanup(settings):
    if not settings.get('DEBUG'):
        settings_composer.set(FOO='bar')
        settings_composer.apply_switch('https', 'on')
        settings_composer.exclude_from_setting('INSTALLED_APPS', ['debug_tools', 'testing_tools'])
```


## Debugging

Large projects can have a lot of settings, and even with the best intentions it's not always clear where a setting may be defined or overriden. Django Settings Composer aims to simplify the act of defining settings, but it also provides new and interesting ways to make settings more complicated if proper care isn't taken.

With that in mind, Django Settings Composer builds a useful property right into the settings.

**SETTINGS_COMPOSER_SOURCE**

This  is a dictionary, where each key is a setting name, and each value is the name of the module (or actions) that was/were responsible for setting it.

If you can't figure out why a setting isn't changing where you expect it to, look it up here.

_Note: Each value in **SETTINGS_COMPOSER_SOURCE** is a list. If a setting is overridden at any point, the final entry will be the source of the current value, and previous entries relate to prior definitions._

```
from django.conf import settings
print settings.SETTINGS_COMPOSER_SOURCE['DEBUG'][-1]

# [SWITCH <debug: off> DEFINED IN settings.definitions LOADED BY settings] SET BY FUNCTION 'clean_up' CALLED FROM settings.clean_up_functions LOADED BY settings
```