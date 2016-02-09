from . import environment
from .helpers import output_if_verbose


def collate_settings_modules():
    """
    Create a list of of settings modules to load, in order, based on settings
    module, site, environment and switch variables.
    """
    settings_module = environment.get_settings_module_name()
    env = environment.get_env_name()
    site = environment.get_site_name()
    switches = environment.get_switches()

    output_if_verbose(
        "Reading environmental variables from OS",
        u"Settings: " + settings_module,
        u"Env: " + env,
        u"Site: " + site,
        u"Switches: " + u', '.join(
            [
                u'%s: %s' % (key, value)
                for (key, value) in switches.items()
            ]
        )
    )

    settings_files = [u'{settings_module}']
    if env:
        settings_files.append(u'{settings_module}.env.{env}')
    if site:
        settings_files.append(u'{settings_module}.sites.{site}')
    if env and site:
        settings_files.append(u'{settings_module}.sites.{site}.env.{env}')
    settings_files = map(
        lambda module_name: module_name.format(
            settings_module=settings_module,
            site=site,
            env=env
        ),
        settings_files
    )

    output_if_verbose(
        "Compiling settings modules based on environmental variables",
        *settings_files
    )

    return settings_files
