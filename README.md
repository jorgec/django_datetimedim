# Django DateTimeDimesion

Django DateTimeDimesion is a droppable Django app for dealing with dates and times as dimension tables.

## Installation

`¯\_(ツ)_/¯`


## Usage

Add to your `INSTALLED_APPS` in `settings.py`:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    ...
    'datetimedim',
    ...
]

```
Use as a `models.ForeignKey` field.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
