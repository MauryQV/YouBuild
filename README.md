PARA INSTALAR DEPENDENCIAS: 
pip install -r requirements.txt


<<ES NECESARIO TENER POSTGRES (arriba de postgres 12.0 >>

EN EL DOCUMENTO setting.py 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'youbuild_system',
        'USER': 'postgres',
        'PASSWORD': '0000',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
REQUISITOS:
crear una base de datos llamada "youbuild_system"
Cambiar segun como esta configurado su postgres

PARA MIGRAR LA BASE DE DATOS:
-ir al proyecto
-ejecutar python manage.py makemigrations
-ejecutar python manage.py migrate

FINALMENTE EJECUTAR
python manage.py runserver
 PARA ADMINISTRAR DESDE localhost:8000/admin
 ejecutar:
 python manage.py createsuperuser 
 seguir los pasos--> iniciar sesion
