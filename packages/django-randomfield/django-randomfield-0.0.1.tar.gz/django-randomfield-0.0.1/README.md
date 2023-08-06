# Django IBAN Field
[![Build Status](https://travis-ci.org/KeoH/django-randomfield.svg?branch=master)](https://travis-ci.org/KeoH/django-randomfield)
[![Coverage Status](https://coveralls.io/repos/github/KeoH/django-randomfield/badge.svg?branch=master)](https://coveralls.io/github/KeoH/django-randomfield?branch=master)

IBANField is an extension for django CharField with special validation for IBAN accounts.

## Install

You can install django-randomfield with pip as usual o pipenv

```bash
    $> pip install django-randomfield
```

```bash
    $> pipenv install django-randomfield
```

## Usage

Use IBANField on your models, like any other django models fields.

```python
    from django_randomfield.fields import CharRandomField

    class MyModel(models.Model):

        account = CharRandomField()
```
