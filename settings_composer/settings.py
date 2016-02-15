# A pseudo-settings file that loads the actual settings files for a project
# based on environment variables

from .loading import collect_settings


collect_settings(globals())
