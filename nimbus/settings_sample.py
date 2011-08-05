#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#Copyright © 2010, 2011 Veezor Network Intelligence (Linconet Soluções em Informática Ltda.), <www.veezor.com>
#
# This file is part of Nimbus Opensource Backup.
#
#    Nimbus Opensource Backup is free software: you can redistribute it and/or 
#    modify it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License.
#
#    Nimbus Opensource Backup is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Nimbus Opensource Backup.  If not, see <http://www.gnu.org/licenses/>.
#
#In this file, along with the Nimbus Opensource Backup code, it may contain 
#third part code and software. Please check the third part software list released 
#with every Nimbus Opensource Backup copy.
#
#You can find the correct copyright notices and license informations at 
#their own website. If your software is being used and it's not listed 
#here, or even if you have any doubt about licensing, please send 
#us an e-mail to law@veezor.com, claiming to include your software.
#


# Django settings for nimbus project.

from os.path import join, dirname

DEBUG = True
TEMPLATE_DEBUG = DEBUG
AJAX_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS


DATABASES = {
    'default': {
        'NAME': '',
        'ENGINE': '',
        'USER' : '',
        'PASSWORD' : '',
        'HOST' : ''
    },
    'bacula' : {
        'NAME' : '',
        'ENGINE' : '',
        'USER' : '',
        'PASSWORD' : '',
        'HOST' : ''
    }
}


### NIMBUS


NIMBUS_MANAGER_URL = "http://localhost:8888"

ROOT_PATH = "/"



NIMBUS_ETC_DIR = join(ROOT_PATH, "etc", "nimbus")
NIMBUS_HOME_DIR = join(ROOT_PATH, "var", "nimbus")

NIMBUS_SSLCONFIG = join(NIMBUS_ETC_DIR, "ssl.conf")



NIMBUS_DEPLOY_PATH = join(ROOT_PATH, "var", "www")
NIMBUS_EXE = join(NIMBUS_DEPLOY_PATH, "nimbus")

BACULA_LOCK_FILE = join(NIMBUS_HOME_DIR, "bacula.lock" )
NIMBUS_GRAPHDATA_FILENAME = join(NIMBUS_HOME_DIR, "graphs.data" )

NIMBUS_DEFAULT_ARCHIVE = '/bacula'

NIMBUS_CUSTOM_DIR = join(NIMBUS_HOME_DIR, "custom" )
NIMBUS_CONFIG_DIR = join(NIMBUS_CUSTOM_DIR, "config" )
NIMBUS_CERTIFICATES_DIR = join(NIMBUS_CUSTOM_DIR, "certificates" )

NIMBUS_JOBS_DIR = join(NIMBUS_CUSTOM_DIR, "jobs" )
NIMBUS_RESTORE_FILE = join(NIMBUS_JOBS_DIR, "restorejob" )

NIMBUS_COMPUTERS_DIR = join(NIMBUS_CUSTOM_DIR, "computers" )
NIMBUS_FILESETS_DIR = join(NIMBUS_CUSTOM_DIR, "filesets" )
NIMBUS_POOLS_DIR = join(NIMBUS_CUSTOM_DIR, "pools" )
NIMBUS_DEVICES_DIR = join(NIMBUS_CUSTOM_DIR, "devices" )
NIMBUS_STORAGES_DIR = join(NIMBUS_CUSTOM_DIR, "storages" )
NIMBUS_SCHEDULES_DIR = join(NIMBUS_CUSTOM_DIR, "schedules" )

BCONSOLE_CONF = join(NIMBUS_CONFIG_DIR, "bconsole.conf")
BACULADIR_CONF = join(NIMBUS_CONFIG_DIR, "bacula-dir.conf")
BACULAFD_CONF = join(NIMBUS_CONFIG_DIR, "bacula-fd.conf")
BACULASD_CONF = join(NIMBUS_CONFIG_DIR, "bacula-sd.conf")
LOGGING_CONF = join(NIMBUS_ETC_DIR, "logging.conf")
INITIALDATA_FILE = join(NIMBUS_HOME_DIR, "initial_data.json")
PYBACULA_TEST = True


NIMBUS_UNDEPLOYED_CONF_FILES = join( dirname(__file__), 'confs')
NIMBUS_UNDEPLOYED_LOG_CONF = join(NIMBUS_UNDEPLOYED_CONF_FILES, "logging.conf")

RESTORE_POINT_DEFAULT = "/tmp/bacula-restore"

NIMBUS_WIZARD = True

# Nimbus log verbose
LOG_DEBUG = True

# Static files
SERVE_STATIC_FILES = True


NIMBUS_CLIENT_PORT = 11110


NIMBUS_CENTRAL_USER_DATA_URL = "http://www.veezor.com/central/acesso_iam.php"


NIMBUS_RELOAD_REQUESTS_THRESHOLD = 20
NIMBUS_MIN_RELOAD_REQUESTS_INTERVAL = 60

RELOAD_MANAGER_PORT = 11113
RELOAD_MANAGER_ADDRESS = '127.0.0.1'
RELOAD_MANAGER_URL = "http://localhost:11113"
RELOAD_MANAGER_START_SLEEP_TIME = 3
RELOAD_MANAGER_COMMAND = [NIMBUS_EXE,'--start-reload-manager-service']
RELOAD_MANAGER_LOGGING_CONF = join(NIMBUS_ETC_DIR, "reload_manager_logging.conf")




# END NIMBUS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = ''

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
if SERVE_STATIC_FILES:
    MEDIA_ROOT = join( dirname(__file__), 'media')
else:
    MEDIA_ROOT = join( NIMBUS_DEPLOY_PATH, 'media' )

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/adminmedia/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '7qj040(6uwuuzx+y&ety-bs5i$*q$0tag02q+sx8th_%1w$h9%'


SESSION_EXPIRE_AT_BROWSER_CLOSE = True

LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "/session/login"


TEMPLATE_CONTEXT_PROCESSORS = (
    "nimbus.shared.contextprocessors.script_name",
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media" ,
    "django.contrib.messages.context_processors.messages"
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'nimbus.shared.middlewares.LogSetup',
    'nimbus.shared.middlewares.ThreadPool',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'nimbus.security.middlewares.AdministrativeModelChangeCatcher',
)


DATABASE_ROUTERS = ['nimbus.bacula.dbrouting.Router']

if AJAX_DEBUG:
    MIDDLEWARE_CLASSES += ('nimbus.shared.middlewares.AjaxDebug' ,)


if NIMBUS_WIZARD:
    MIDDLEWARE_CLASSES += ('nimbus.wizard.middleware.Wizard' ,)


ROOT_URLCONF = 'nimbus.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'nimbus.bacula',
    'nimbus.session',
    'nimbus.base',
    'nimbus.users',
    'nimbus.config',
    'nimbus.network',
    'nimbus.schedules',
    'nimbus.filesets',
    'nimbus.storages',
    # 'nimbus.pools',
    'nimbus.procedures',
    'nimbus.timezone',
    'nimbus.wizard',
    'nimbus.computers',
    # 'nimbus.backup',
    'nimbus.restore',
    'nimbus.system',
    'nimbus.security',
    'south'
)

if DEBUG:
    INSTALLED_APPS += ("django.contrib.admin",)
