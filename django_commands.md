# Django commands

### Arrancar proyecto
```bash
django-admin startproject NOMBRE_PROYECTO
```

### Correr server
```bash
python manage.py runserver
```

### Crear app
```bash
python manage.py startapp NOMBRE_APP
```

### Migrar 
Crear tablas de bbdd y otras dependencias de INSTALLED_APPS en settings.py
```bash
python manage.py migrate
```

### Agregar app models a bbdd
```bash
python manage.py makemigrations NOMBRE_APP
```

### sqlmigrate
Toma la data de migration de la app y crea el codigo SQL (no lo ejecuta)
```bash
python manage.py sqlmigrate NOMBRE_APP NUMERO
```