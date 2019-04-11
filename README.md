# Flask-BS4

***This is a fork of [Flask-Bootsrap](https://pypi.org/project/Flask-Bootstrap/) upgraded to Bootstrap 4.x.x.***

Flask-Bootstrap packages [Bootstrap](http://getbootstrap.com) into an extension that mostly consists of a blueprint named `bootstrap`. It can also create links to serve Bootstrap from a CDN and works with no boilerplate code in your application.


## Usage

Here is an example:  

```python
from flask_bs4 import Bootstrap

[...]

Bootstrap(app)
```

This makes some new templates available, containing blank pages that include all bootstrap resources, and have predefined blocks where you can put your content.

As of version 3, Flask-Bootstrap has a [proper documentation](http://pythonhosted.org/Flask-Bootstrap), which you can check for more details.