rivr-jinja
==========

[![Build Status](http://img.shields.io/travis/rivrproject/rivr-jinja/master.svg?style=flat)](https://travis-ci.org/rivrproject/rivr-jinja)

An extension to rivr for using the Jinja template engine.

## Installation

```bash
$ pip install rivr-jinja
```

## Usage

```python
from rivr_jinja import *
```

### View

Example, registering the template `about.html` with the `/about` endpoint in
our router:

```python
@router.register(r'about')
JinjaView.as_view(template_name='about.html')
```

Sub-classing `JinjaView`:

```python
class View(JinjaView):
    template_name = 'about.html'
```

```python
class View(JinjaView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        return {
            'template': 'variable'
        }
```

### Middleware

To attach a Jinja environment to any `JinjaResponse`, use the `JinjaMiddleware`.

```python
from jinja2 import Environment, DictLoader

loader = DictLoader({'index.html': 'Hello {{ name }}'})
environment = Environment(loader=loader)

middleware = JinjaMiddleware(environment)
```

### Response

```python
JinjaResponse(request, template_names=['index.html'], context={'name': 'World'})
```

## License

rivr-jinja is released under the BSD license. See [LICENSE](LICENSE).

