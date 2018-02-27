import os
from os import environ

import dj_database_url

import otree.settings


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# the environment variable OTREE_PRODUCTION controls whether Django runs in
# DEBUG mode. If OTREE_PRODUCTION==1, then DEBUG=False
if environ.get('OTREE_PRODUCTION') not in {None, '', '0'}:
    DEBUG = False
else:
    DEBUG = True

# disabling debug in hard-coded fashion for now:
DEBUG = False

ADMIN_USERNAME = 'NBU'

# for actual study, change this to strong password using ENV not settings.py:
ADMIN_PASSWORD = "default"

# for security, best to set admin password in an environment variable
# ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

# don't share this with anybody.
SECRET_KEY = "ssq!u#scxer8j+@mr@ehj=8ai)#_m_1)p^%gzf*3#^*s^ti5no"

DATABASES = {
    'default': dj_database_url.config(
        # Rather than hardcoding the DB parameters here,
        # it's recommended to set the DATABASE_URL environment variable.
        # This will allow you to use SQLite locally, and postgres/mysql
        # on the server
        # Examples:
        # export DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/NAME
        # export DATABASE_URL=mysql://USER:PASSWORD@HOST:PORT/NAME

        # fall back to SQLite if the DATABASE_URL env var is missing
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    )
}

# AUTH_LEVEL:
# If you are launching a study and want visitors to only be able to
# play your app if you provided them with a start link, set the
# environment variable OTREE_AUTH_LEVEL to STUDY.
# If you would like to put your site online in public demo mode where
# anybody can play a demo version of your game, set OTREE_AUTH_LEVEL
# to DEMO. This will allow people to play in demo mode, but not access
# the full admin interface.

# Set via environment variables:
# AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

AUTH_LEVEL = "DEMO"

# setting for integration with AWS Mturk
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')


# e.g. EUR, CAD, GBP, CHF, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = True


# e.g. en, de, fr, it, ja, zh-hans
# see: https://docs.djangoproject.com/en/1.9/topics/i18n/#term-language-code
LANGUAGE_CODE = 'en'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

# SENTRY_DSN = ''

DEMO_PAGE_INTRO_TEXT = """
oTree games
"""

mturk_hit_settings = {
    'keywords': ['easy', 'bonus', 'choice', 'study'],
    'title': 'Title for your experiment',
    'description': 'Description for your experiment',
    'frame_height': 500,
    'preview_template': 'global/MTurkPreview.html',
    'minutes_allotted_per_assignment': 60,
    'expiration_hours': 7*24,  # 7 days
    # 'grant_qualification_id': 'YOUR_QUALIFICATION_ID_HERE',# to prevent retakes
    # to use qualification requirements, you need to uncomment the 'qualification' import
    # at the top of this file.
    'qualification_requirements': [],
}

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.000,
    'participation_fee': 0.00,
    'mturk_hit_settings': mturk_hit_settings,
    'use_browser_bots': False,
    'doc': "TBC",
}


SESSION_CONFIGS = [
    { 
        'name': 'dictator_bt',
        'display_name': 'Single Player Dictator Experiment / version bt',
        'app_sequence': ['dictator_bt'],
        'num_rounds': 3,
        'num_demo_participants': 1,
    },
    { 
        'name': 'dictator_modified',
        'display_name': '3 Player Dictator Experiment / version reg',
        'app_sequence': ['dictator_modified'],
        'num_rounds': 3,
        'num_demo_participants': 3,
    },
        { 
    'name': 'dictator_sp',
    'display_name': 'TEST (ONGOING) - Incentivised 2-player Dictator Experiment / version tp',
    'app_sequence': ['dictator_sp'],
    'num_rounds': 3,
    'num_demo_participants': 2,
    },
]

ROOM_DEFAULTS = {}

ROOMS = [
    {
        "name": "NBU_test",
        "display_name": "NBU modified dictator test room",
        "participant_label_file": "session_changes/participant_label_file.txt",
    },
]
# anything you put after the below line will override
# oTree's default settings. Use with caution.
otree.settings.augment_settings(globals())

