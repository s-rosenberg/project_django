### urls.py 
path() args:
    - route: url pattern. cuando se procesa una request se busca entre los routes de urlpatterns hasta que matchee.
            solo se fija en el pattern sin tener en cuenta parametros o domainname
    - view: si matchea la request con un pattern (route) llama a una view en especficio

### settings.py
manejar module-level variables
entre ellas: bbdd configurations
por default toma SQLite. Esta buena para pruebitas pero no se recomienda para real development
para cambiar y mas doc https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-DATABASES

### secrets
no pushear el SECRET_KEY -> se puede usar variables de entorno (para development, no conviene para produ)

## models
model es la unica y definitiva fuente de informacion sobre la data. contiene los campos esecnciales y comportamientos de la data guardada
se arma como clase donde cada atributo es un campo dentro de la tabla 
los campos son objetos de la clase Field.
- el primer positional argument es el 'human-readable name'. Si no es provisto, queda el machine-readable name que es el nombre del attr
- para denotar una relacion usar ForeingKey como tipo de Field.

### activating models
para incluir la app dentro del project hay que agregarlo a installed apps en el settings.py
makemigrations sirve para que Django sepa que se generaron cambios en los modelos
genera un archivo num_initial.py con la data de los modelos a crear

**hint:** *python manage.py check checkea si habra problemas sin realizar la migracion* 

### filtros
para filtrar un queryset por atributo de modelos se usa:
`ATTR_NAME__OPERADOR`
con el doble "_" entre uno y otro.
[Lista de operadores](https://www.w3schools.com/django/django_queryset_filter.php)


# Testing

## rule of thumb xd

- separate TestClass for each model or view
- a separate test method for each set of conditions you want to test
- test method names that describe their function
