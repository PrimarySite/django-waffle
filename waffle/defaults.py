from __future__ import unicode_literals


COOKIE = 'dwf_%s'
TEST_COOKIE = 'dwft_%s'
SECURE = True
MAX_AGE = 2592000  # 1 month in seconds

CACHE_PREFIX = 'waffle:'
CACHE_NAME = 'default'
FLAG_CACHE_KEY = 'flag:%s'
FLAG_USERS_CACHE_KEY = 'flag:%s:users'
FLAG_GROUPS_CACHE_KEY = 'flag:%s:groups'
ALL_FLAGS_CACHE_KEY = 'flags:all'
SAMPLE_CACHE_KEY = 'sample:%s'
ALL_SAMPLES_CACHE_KEY = 'samples:all'
SWITCH_CACHE_KEY = 'switch:%s'
ALL_SWITCHES_CACHE_KEY = 'switches:all'

FLAG_DEFAULT = False
SAMPLE_DEFAULT = False
SWITCH_DEFAULT = False

READ_FROM_WRITE_DB = False

CREATE_MISSING_FLAGS = False
CREATE_MISSING_SAMPLES = False
CREATE_MISSING_SWITCHES = False

LOG_MISSING_FLAGS = None
LOG_MISSING_SAMPLES = None
LOG_MISSING_SWITCHES = None

OVERRIDE = False

UNIQUE_FLAG_NAME = True
