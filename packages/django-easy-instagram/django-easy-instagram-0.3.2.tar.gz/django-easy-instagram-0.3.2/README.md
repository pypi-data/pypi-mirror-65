# django-easy-instagram

A Django application that provides a template tag for displaying content from a public Instagram profile. Has ability to cache files locally.

This is derived from [Marco Pompili's version](https://github.com/marcopompili/django-instagram), which has different requirements and options. Thanks to Marco for doing all the hard work.

## Requirements

*   [Django >= 1.6](https://www.djangoproject.com/)
*   [html5lib](https://pypi.python.org/pypi/lxml/3.6.4)
*   [requests](https://pypi.python.org/pypi/requests/2.11.1)
*   [sorl-thumbnail](https://github.com/mariocesar/sorl-thumbnail)
*   [Pillow](https://pypi.python.org/pypi/Pillow/3.3.1)

## Installation

Install Django with your favourite Linux packaging system or you can use pip for installing python packages, if Django is not an official package for your distribution:

```bash
pip install django
```

Use pip to install Django Easy Instagram:

```bash
pip install django-easy-instagram
```

Pip should take care of the package dependencies for Django Easy Instagram.

## Configuration

Add the application to INSTALLED_APPS:

```python
  INSTALLED_APPS = (
    ...
    'sorl.thumbnail', # required for thumbnail support
    'django_easy_instagram',)
```

Rebuild your application database, this command depends on which version of Django you are using.

In Django 2.0 (recommended):

```bash
python manage.py makemigrations django_easy_instagram
```

Them migrate the db:

```bash
python manage.py migrate
```

## Usage

The `instagram_user_recent_media` brings into context two objects:
  - `profile`: Contains the who scraped object.
  - `recent_media`: Contains the recent media, like 10 or 12 entries or so.

You can display the data contained in `recent_media` list like this:

```html
<!DOCTYPE html>

{% load instagram_client %}

<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ instagram_profile_name|capfirst }} Instagram feed</title>
</head>
<body>
<h1>{{ instagram_profile_name|capfirst }} Instagram Feed</h1>
<div id="django_recent_media_wall">
    {% instagram_user_recent_media instagram_profile_name %}
    {% for media in recent_media %}
        <div class="django_easy_instagram_media_wall_item">
            <a href="//instagram.com/p/{{ media.shortcode }}" target="_blank">
                <img src="{{ media.thumbnail_src }}"/>
                <span>{{ media.edge_media_to_caption.edges.0.node.text }}</span>
            </a>
        </div>
    {% endfor %}
</div>
<p>Got from instagram</p>
</body>
</html>
```

## Resizing and Caching Images

You are able to resize images, which will also mean they are cached locally rather than being loaded from Instagram's servers.

To enable this, ensure you have `sorl.thumbnail` in the INSTALLED_APPS, and that you have setup [Django caching](https://docs.djangoproject.com/en/2.2/topics/cache/).

In order for requests to Instagram to work properly, you will need to ensure you set the `sorl.thumbail` setting:

```bash
THUMBNAIL_REMOVE_URL_ARGS = False
```

You can then use the `local_cache` template filter and specify a size:

```html
{% for media in recent_media %}
...
<img src="{{ media.thumbnail_src|local_cache:'332x332' }}"/>
...
{% endfor %}
```

The images will be saved locally in a cache.

By default images will be resized and saved at 80% JPG quality, to
override this you can use this setting in your Django settings file:

```bash
INSTAGRAM_QUALITY = 90
```

## Thanks

The original version and most of the actual work was done by Marco Pompili in the version [available here](https://github.com/marcopompili/django-instagram).
