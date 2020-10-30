# POLP TODO

* [ ] **Trust relationships**

  * [ ] Refactor DRY

    *There are two pairs of functions that can be put together because their logic is very similar ** (service, account) ** and ** (roles, users) **. The idea is to reduce those 4 functions to at least 2.* 

  * [ ] Modular Refactor

    *It would be nice if the logic for updating trust relationships is separate from `update_roles`.*

  * [x] Testear para mergear a develop

* [x] **Preguntas DB performance.**

  *La idea es juntarnos con alguien que sepa bastante de base de datos y ver de hacerle algunas consultas de performance. Estaría bueno preguntarle lo siguiente*

  * [x] Check Object en memoria vs Pedir * Roles post role_update() Que tan costoso es eso que estamos haciendo ?
  * [x] Que es mejor guardar ? Epoch time o Datetime ?
  * [x] Que columnas nos conviene indexar ? (Contar que queries vamos a querer hacer)
  * [x] Queriar Roles por servicios. 
  * [x] Caching de queries ?    
  * [x] Vistas ayudan a la performance o solo simplifican las queries ?
  * [x] *Ver que queries queremos revisar y cuales no nos salen.* 

* [x] **Métricas**

  * [x] Dashboard solamente de KPI
  * [x] Que roles estan fuera de estandar ?
  * [x] Más métricas críticas
  * [ ] Add Description to each grafana graph
  * [x] Deploy Grafana

* [ ] **Drastically reduce DRY code**

  *The IAM Model (Service / IAM) calls different objects that essentially do the same thing. There is code that I think could not be repeated and simplified like the functions that handle calls to AWS and their pagination (`marker_handler`). To use rate limiter or the `cluoudaux` pager that we are already using when we request the last_used of the policies.*

* [x] **POLP Open source :open_book:**

  *Hay algunas cosas que deberíamos tener en cuenta antes de hacer el proyecto open source.*

  * [x] Sacar todo lo relativo a Fury
    * [x] CI/CD files
      * [x] Carpeta commands
    * [x] Dockerfile
    * [x] Dockerfile.runtime
    * [x] +
  * [x] Remover dependencias de newrelic
  * [x] Remover bash scripts (`create.sh`, `migrate.sh`, etc)
  * [x] Documentación

* [x] **Configuration**

  * [x] Take all configurations to `config.py` 
    * [x] Database conf string
    * [x] Roles

* [x] **Last Used for Roles**

  This issue explains why we would not get the Roles https://github.com/boto/boto3/issues/2297	

  * [x] Make the apicall get_role() for each role.

* [x] Check conditions for roles

* [ ] **Refactor de Accounts Controller**

  * [x] Use find or create

  * [ ] AccountUpdater ?

    Vale la pena hacer  un Account Updater ? **Pro:** Nos queda un código consistente con el resto de los jobs **Con:** Tiempo, retestear

* [x] **Evaluate update methodology**

  Currently we are deleting old row by filtering the `job_uuid` column which is present in most rows in the DB
