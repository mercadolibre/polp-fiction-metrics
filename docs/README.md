# POLP TODO

* [ ] **Trust relationships**

  * [ ] Refactor DRY

    *There are two pairs of functions that can be put together because their logic is very similar ** (service, account) ** and ** (roles, users) **. The idea is to reduce those 4 functions to at least 2.* 

  * [ ] Modular Refactor

    *It would be nice if the logic for updating trust relationships is separate from `update_roles`.*

* [ ] **Métricas**
  * [ ] More metrics with service segregation

* [ ] **Drastically reduce DRY code**

  *The IAM Model (Service / IAM) calls different objects that essentially do the same thing. There is code that I think could not be repeated and simplified like the functions that handle calls to AWS and their pagination (`marker_handler`). To use rate limiter or the `cluoudaux` pager that we are already using when we request the last_used of the policies.*

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


* [x] **Evaluate update methodology**

  Currently we are deleting old row by filtering the `job_uuid` column which is present in most rows in the DB
