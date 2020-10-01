import os
import socket

# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']

basedir = os.path.abspath(os.path.dirname(__file__))

ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
ENABLE_CORS = os.getenv('ENABLE_CORS', True)

# ==================== LOGGING ============================================
ENABLE_SLACK_LOGGING = os.getenv("ENABLE_SLACK_LOGGING", "false")
LOG_LEVEL = os.getenv('LOGGING_LEVEL', 'DEBUG')
LOGGING_SLACK_API_KEY = os.getenv('SLACK_API_KEY', "slack api key")
LOGGING_SLACK_CHANNEL = "#flask-app-" + ENVIRONMENT
LOG_DIR = 'log'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "%(levelname)-7s [%(asctime)s] [%(module)s.%(funcName)s:%(lineno)d] : %(message)s"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'app.DEBUG': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': LOG_DIR + '/app.DEBUG.log',
            'maxBytes': 30 * 1024 * 1024,  # 1Kb       #100 * 1024 * 1024,  # 100Mb
            'backupCount': 3,
        },
        'app.INFO': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': LOG_DIR + '/app.INFO.log',
            'maxBytes': 30 * 1024 * 1024,  # 1Kb       #100 * 1024 * 1024,  # 100Mb
            'backupCount': 3,
        },
        'app.ERROR': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': LOG_DIR + '/app.ERROR.log',
            'maxBytes': 30 * 1024 * 1024,  # 1Kb       #100 * 1024 * 1024,  # 100Mb
            'backupCount': 3,
        },
        'celery.DEBUG': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': LOG_DIR + '/celery.DEBUG.log',
            'maxBytes': 30 * 1024 * 1024,  # 1Kb       #100 * 1024 * 1024,  # 100Mb
            'backupCount': 3,
        },
        'celery.ERROR': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': LOG_DIR + '/celery.ERROR.log',
            'maxBytes': 30 * 1024 * 1024,  # 1Kb       #100 * 1024 * 1024,  # 100Mb
            'backupCount': 3,
        },
        'slack.ERROR': {
            'level': 'ERROR',
            'api_key': LOGGING_SLACK_API_KEY,
            'class': 'slacker_log_handler.SlackerLogHandler',
            'channel': LOGGING_SLACK_CHANNEL,
            'username': 'brandlytic-{}-{}'.format(socket.gethostname(), ENVIRONMENT)
        },
    },
    'loggers': {
        'app': {
            'handlers': ['console', 'app.DEBUG', 'app.ERROR', 'slack.ERROR'] if ENABLE_SLACK_LOGGING == 'true' else ['console', 'app.DEBUG', 'app.ERROR'],
            'propagate': False,
            'level': 'INFO',
        },
        'celery': {
            'handlers': ['console', 'celery.DEBUG', 'celery.ERROR', 'slack.ERROR'] if ENABLE_SLACK_LOGGING == 'true' else ['console', 'celery.DEBUG', 'celery.ERROR'],
            'propagate': False,
            'level': 'INFO',
        },
        'root': {
            'handlers': ['console', 'celery.DEBUG', 'celery.ERROR', 'app.DEBUG', 'slack.ERROR'] if ENABLE_SLACK_LOGGING == 'true'else ['console', 'celery.DEBUG', 'celery.ERROR', 'app.DEBUG'],
            'propagate': False,
            'level': 'INFO',
        }
    }
}

# ==================== DATABASE ===========================================
POSTGRES_HOST = os.getenv('POSTGRES_AUTH_HOST', '127.0.0.1')
POSTGRES_DB = os.getenv('POSTGRES_AUTH_DB', 'kidssy-account')
POSTGRES_USER = os.getenv('POSTGRES_AUTH_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_AUTH_PASSWORD', '89shuey27h3gf8')
POSTGRES_PORT = os.getenv('POSTGRES_AUTH_PORT', 5432)
DATABASE_ECHO = os.getenv('DATABASE_ECHO', 'yes')
DATABASE_URL = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}".format(
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    database=POSTGRES_DB
)

# ==================== RABBITMQ ===========================================
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', '127.0.0.1')
RABBITMQ_PORT = os.getenv('RABBITMQ_PORT', 5672)
RABBITMQ_URL = 'amqp://guest@' + RABBITMQ_HOST + ':' + str(RABBITMQ_PORT) + '//'

# ==================== REDIS ===========================================
REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = os.getenv('REDIS_PORT', 6380)
REDIS_URL = "redis://{host}:{port}".format(host=REDIS_HOST, port=REDIS_PORT)

# ==================== CELERY ===========================================
# CELERY_BROKER_URL = REDIS_URL
# CELERY_RESULT_BACKEND = REDIS_URL
CELERY_BROKER_URL = RABBITMQ_URL
CELERY_RESULT_BACKEND = RABBITMQ_URL


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False


class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '../../flask_boilerplate_main.db')
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}".format(
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DB
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '../../flask_boilerplate_test.db')
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{user}:{password}@{host}/{database}".format(
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        database=POSTGRES_DB
    )
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY


# SEND MAIL
MAIL_USERNAME = 'sigmasolutions.eu@gmail.com'
MAIL_PASSWORD = 'sigmasolutionseu'
MAIL_NAME='KIDSSY'
mail_settings = {
    'MAIL_SERVER' : 'smtp.gmail.com',
    'MAIL_PORT' : 587,
    'MAIL_USE_TLS' : True,
    'MAIL_USE_SSL' : False,
    'MAIL_USERNAME' : os.getenv('MAIL_USERNAME', MAIL_USERNAME),
    'MAIL_PASSWORD' : os.getenv('MAIL_PASSWORD', MAIL_PASSWORD),
    'MAIL_DEFAULT_SENDER' : os.getenv('MAIL_DEFAULT_SENDER', MAIL_USERNAME)
}

class AuthConfig:
    ADMIN_KEY = 'STjSejeZ3GIvewdIHxfSphi4V2u0XZzw'
    ADMIN_SECRET = 'pXvDKSRnzKTai8WwY9xPmm0J4UXVibuZ'
    PROVIDER_KEY = 'P7XWebTdpmCk7fRI2nAawqk4qXvTJC6y'
    PROVIDER_SECRET = 'Hz6nAAVoznIWlFZqEjhSAeFXH90VhwMD'
    USER_KEY = 'n1rHRma0vduYSs1vuNzKdVufbkleL7gu'
    USER_SECRET = 'gvWOcI9eoDeHX3aDeJ6dD1PnSH6MDEVr'
    EXP_TIME =1