# django-settings-composer
A 'sensible' way to gather settings dynamically.

## Rationale

Django allows developers to reference only a single settings file, and leaves it entirely up to the developers to contrive a way to make their settings dynamic based on environmental or other settings.

> We don't need a default solution for this. It's not within the scope of this project to tell people how they should organize their settings files. Take that opportunity to showcase your individualism." <cite>Adrian Holovaty, Django co-creator</cite>

That's all very well, and unique development environments often require bespoke solutions, but most of us are trying to solve the same problem without any established pattern to do so. The result is complex and hard to follow settings files, with duplication and multiple chains of inheritence.

Django Settings Composer seeks to provide:

- minimal setup
- maximum flexibility
- the exact same syntax as standard Django settings (no class inheritence)
- clear, consistent override rules
- introspection to see exactly how a given Django Settings object was compiled

Django Settings Composer allows you to:

1. define project wide global settings and defaults
2. suplement or override these with site-specific settings
3. define environment-specific settings such as databases and keys
4. 'switch on' specific settings groups, such as debug mode or use a sqlite database
5. exclude certain apps, middleware etc. for specific setups

## Setup

You can use as much or as little of the customisablity as you require. Django Settings Composer merely provides a basic framework and a few conventions to follow. The setting loader logic will look for files based on a particular permutation of environmental variables, but it doesn't care if individual files are missing, so only create the files you need.

The loading logic is as follows:

1. A project-wide settings module
2. A project-wide, environment-specific settings module
3. A site-specific settings module
4. A site-specific, environment-specific settings module
5. A settings module per 'switch'
6. An optional final module, for custom clean-up

### Environment variables

Firstly, point Django to the settings composer settings file.

```
export DJANGO_SETTINGS_MODULE=settings_composer.settings
```

Then you only really need to set one other environment variable to get going:

**SETTINGS_COMPOSER_PROJECT**

This is the python module that represents your django project, or more accurately, the module that directly contains a _settings_ module.

```
export SETTINGS_COMPOSER_PROJECT=myproject

# But, if your settings module is a submodule of conf, for example
# export SETTINGS_COMPOSER_PROJECT=myproject.conf 
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

This is a comma separated list of settings files within _myproject.settings.switches_. These only exist on a project-wide basis as the idea is to give you a clean way of turning features on and off regardless of your current site or environment.

```
export SETTINGS_COMPOSER_SWITCHES=debug_off,test_db
```

**SETTINGS_COMPOSER_VERBOSE**

If set to 'true' or 'yes', Django Settings Composer will report each step it takes throughout the loading phase to **stdout**.

```
export SETTINGS_COMPOSER_VERBOSE=yes
```

### A really simple project layout

```
export SETTINGS_COMPOSER_PROJECT=myproject
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

### A simple project layout with multiple sites and some switches

```
export SETTINGS_COMPOSER_PROJECT=myproject
export SETTINGS_COMPOSER_SITE=site_1
export SETTINGS_COMPOSER_SWITCHES=debug_off
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
            switches/
                __init__.py
                debug_off.py
                debug_on.py
```

### A more complex project layout

```
export SETTINGS_COMPOSER_PROJECT=myproject
export SETTINGS_COMPOSER_SITE=site_2
export SETTINGS_COMPOSER_ENV=staging
export SETTINGS_COMPOSER_SWITCHES=debug_on,https_off
```

```
manage.py
    myproject/
        __init__.py
        urls.py
        wsgi.py
        settings/
            __init__.py  <-- imports * from globals and defaults
            globals.py
            defaults.py
            finally.py
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
                site_2/
                    __init__.py
                    env/
                        __init__.py
                        local.py
                        staging.py
                        production.py
                    __init__.py
            switches/
                debug_off.py
                debug_on.py
                https_off.py
                https_on.py
                no_debug_toolbar.py
                test_db.py
```

The above setup will load the following settings modules, in order:

```
myproject.settings
myproject.settings.env.staging
myproject.settings.sites.site_2
myproject.settings.sites.site_2.env.staging
myproject.settings.switches.debug_on
myproject.settings.switches.https_off
myproject.settings.finally
```

This may seem somewhat complex, but that is the nature of building flexibility into code. The important things to remember are:

- There is no inheritence to work out, just a fixed loading order
- If a settings file is not required for a particular permutation, don't include it
- Each file works like any other self-contained Django settings file
- You can put settings directly in an init file, or you can import from sub-modules if you'd prefer to be more organised

_Note: Use **finally.py** only for logic such as compiling a final setting once all other settings have been loaded. It should go without saying that applying a setting here, such as **DEBUG**, will override any other definitions regardless of environmental settings files._

## Debugging

Large projects can have a lot of settings, and even with the best intentions it's not always clear where a setting may live or be overriden. With that in mind, Django Settings Composer builds some useful properties right into the settings.

**SETTINGS_COMPOSER_FILES**

These are the files that Django Settings Composer loaded, or attempted to load, in order. Each item is a 2-tuple containing the module name, and a flag to say whether or not that module was succesfully loaded.

**SETTINGS_COMPOSER_ORIGIN**

This ought to be the silver bullet in your settings-debugging arsenal. It is a dictionary, where each key is a setting name, and each value is the name of the module (or modules in some cases) that was/were responsible for setting it.

If you can't figure out why a setting isn't changing where you expect it to, look it up here.

### Verbose mode

For a detailed report of what Django Settings Composer did, as well as the environmental variables it encountered, turn on verbose mode through the **SETTINGS_COMPOSER_VERBOSE** environmental variable.

## Advanced usage

It is very much by design that individal settings files aren't aware of other settings files. This is in order to minimise the complication of inheritence.

With that said, there are certain situations where you want to adjust a previously defined setting without redefining it, which would be both complicated and non-DRY. Notable settings that are likely to fall into this category include **INSTALLED_APPS** and **MIDDLEWARE_CLASSES**.

For settings that are either lists or dictionaries, you can opt to exclude previously defined values, or add/update them with new values.

Each time Django Settings Composer encoutners one of these modifying settings, it will _combine it with any previously encountered settings of the same name_. Then, when all settings files have been loaded, the modifications will be applied against the target setting.

_Note that you will be able to use **SETTINGS_COMPOSER_ORIGIN** to see all of the settings files that contribute to a modification setting_

### Exclude

From a design point of view, it is often clearer to include everything in your core project settings, and then exclude things if you don't need them, such as debug or testing tools. Certainly in the case of middleware, where loading order is important, this is the only way to have it both ways (i.e. control whether something goes in and what order it goes in relative to everything else.)

Depending on whether the setting being targetted for exclusion is an iterable or a dictionary, the exclusion list(s) you define will contain either the item to remove, or the name of a key to delete.

In practical terms, simply define a setting **SETTINGS_COMPOSER_EXCLUDE_(SETTING_NAME)**. For example:

```
SETTINGS_COMPOSER_EXCLUDE_INSTALLED_APPS = ['debug_toolbar']
SETTINGS_COMPOSER_EXCLUDE_MIDDLEWARE_CLASSES = ['debug_toolbar.middleware.DebugToolbarMiddleware']

```

### Update

Update definitions can be used to either add items to a list, or to insert key-value pairs into a dictionary. This is most useful if you want to override a particular dictionary entry without having to worry about other potential entries.

You could also use it to add further items to **INSTALLED_APPS** for example, but for reasons stated above, you might want to use an exclusion rule instead. Ultimately it is a matter of preferred convention.

To update an existing setting, define a setting **SETTINGS_COMPOSER_UPDATE_(SETTING_NAME)**. For example:

```
SETTINGS_COMPOSER_UPDATE_DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test',
    }
}
SETTINGS_COMPOSER_UPDATE_SECURE_PROXY_SSL_HEADER = ('https')

```

_Note: You must define the original setting before attempting to update it._