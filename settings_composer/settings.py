# A pseudo-settings file that loads the actual settings files for a project
# based on environment variables

from .helpers import (
    collate_settings_modules,
    apply_settings_module,
    apply_updates,
    apply_exclusions
)

SETTINGS_COMPOSER_MODULES = []
SETTINGS_COMPOSER_ORIGIN = {}

for i, settings_module in enumerate(collate_settings_modules()):
    applied_settings = apply_settings_module(
        settings_module,
        globals(),
        SETTINGS_COMPOSER_ORIGIN
    )
    # Processed entries are a tuple of module name and success flag
    if applied_settings is None:
        SETTINGS_COMPOSER_MODULES.append((settings_module, False))
    else:
        SETTINGS_COMPOSER_MODULES.append((settings_module, True))
        SETTINGS_COMPOSER_ORIGIN.update(applied_settings)

apply_updates(globals())
apply_exclusions(globals())
