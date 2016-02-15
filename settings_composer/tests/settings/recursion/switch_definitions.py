import settings_composer


settings_composer.create_switch(
    'recursive', 'loading',
    {'RECURSIVE_LOADING': True}
)
