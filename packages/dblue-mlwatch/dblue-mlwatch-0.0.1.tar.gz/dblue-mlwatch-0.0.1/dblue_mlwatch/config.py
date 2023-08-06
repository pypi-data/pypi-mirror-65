import os

from decouple import config

# Constants
API_KEY_HEADER = 'X-API-KEY'

# Configs
ACCOUNT = config('DBLUE_MLWATCH_ACCOUNT', default=None)
PROJECT = config('DBLUE_MLWATCH_PROJECT', default=None)
API_KEY = config('DBLUE_MLWATCH_API_KEY', default=None)
ENDPOINT = config('DBLUE_MLWATCH_ENDPOINT', default='https://us-central1-dblue-dev-235513.cloudfunctions.net/collect')
METRICS_TRACKING_INTERVAL = config('DBLUE_MLWATCH_METRICS_TRACKING_INTERVAL', default=5, cast=int)

LOG_LEVEL = config("LOG_LEVEL", default="INFO")

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
