### urls.py 
path() args:
    - route: url pattern. cuando se procesa una request se busca entre los routes de urlpatterns hasta que matchee.
            solo se fija en el pattern sin tener en cuenta parametros o domainname
    - view: si matchea la request con un pattern (route) llama a una view en especficio

### settings.py
manejar module-level variables
entre ellas: bbdd configurations
