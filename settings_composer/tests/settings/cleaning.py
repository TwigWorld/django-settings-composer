import settings_composer


LOADED_CLEANING_FUNCTIONS = True


# Load and set


def clean(settings):
    settings_composer.update_setting('STUFF', something='anything')
    settings_composer.exclude_from_setting('STUFF', ['nothing'])


settings_composer.clean(clean)
