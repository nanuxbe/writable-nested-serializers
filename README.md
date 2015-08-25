# writable-nested-serializers (WIP - not production ready)

The code in this application has been inspired (a lot) by https://github.com/miki725/django-rest-framework-bulk

## Sample application installation instructions


- clone this repository
- build venv (optional)
- ``pip install -r requirements.txt``
- ``./manage.py migrate``

## What does the sample application do?

The sample application gives you a simple api available at http://localhost:8000/api/v1/ with writeable nested serializers example.

You can:

- update existing records (owner field is then required on Pet records)
- create new records (owner field should not be included on Pet records)
- delete records

## ToDo

- When using ``PUT``, "missing" related records are deleted. There should be a check to set the ForeignKey to None if ``null=True``
- Test with ManyToMany
- Add a check to validate that the foreign key provided in related records (if any) is the id of the main record
- Write tests
- Write documentation
- Write sample Ember app
