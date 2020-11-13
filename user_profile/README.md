Custom user migration
---------------------


1. Add `user_profile` application to `settings.py` `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    ...,
    'user_profile',
    ...,
]
``` 

2. Set `AUTH_USER_MODEL` value to model reference in `settings.py`

```python
AUTH_USER_MODEL = 'user_profile.User' 
```

3. Custom user migration will be applied before other migrations:

```bash
./manage.py migrate

  Applying user_profile.0001_initial... OK
Operations to perform:
  Apply all migrations: ...
Running migrations:
  No migrations to apply.
```
