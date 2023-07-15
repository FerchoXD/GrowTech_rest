import os
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

MYSQL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
        'OPTIONS': {
            'sql_mode': 'STRICT_TRANS_TABLES',
        },  
    },
}