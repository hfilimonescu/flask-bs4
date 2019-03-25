from flask import Blueprint


class Bootstrap(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('BOOTSTRAP_USE_MINIFIED', True)
        app.config.setdefault('BOOTSTRAP_SERVE_LOCAL', True)

        app.config.setdefault('BOOTSTRAP_LOCAL_SUBDOMAIN', None)

        blueprint = Blueprint('bootstrap',
                              __name__,
                              template_folder='templates',
                              static_url_path=app.static_url_path + '/bootstrap',
                              subdomain=app.config['BOOTSTRAP_LOCAL_SUBDOMAIN'])

        app.register_blueprint(blueprint)

        if not hasattr(app, 'extensions'):
            app.extensions = {}
