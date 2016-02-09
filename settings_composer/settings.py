# A pseudo-settings file that loads the actual settings files for a project
# based on environment variables

from . import settings_manager
from .loading import collate_settings_modules

# Apply settings to current module
settings_manager.bind(globals())
settings_manager.apply_settings_modules(collate_settings_modules())

# Define custom settings
SETTINGS_COMPOSER_SOURCE = settings_manager.settings_source

# Cleanup
settings_manager.unbind()
