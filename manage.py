#!/usr/bin/env python
import os

from flask_script import Manager

from some_app import app

manager = Manager(app)


@manager.command
def runserver(host='0.0.0.0', port=None):
    """Starts a lightweight development Web server on the local machine."""
    if host == 'localhost':
        host = '127.0.0.1'

    default_port = 8080
    port = int(port) if port else default_port

    app.run(debug=True, host=host, port=port)


@manager.command
def rungunicorn(config):
    """Runs the app within Gunicorn."""
    from gunicorn.app.base import Application

    class FlaskApplication(Application):
        def init(self, parser, opts, args):
            cfg = self.get_config_from_module_name(config)
            clean_cfg = {}
            for k, v in cfg.items():
                # Ignore unknown names
                if k not in self.cfg.settings:
                    continue
                clean_cfg[k.lower()] = v
            return clean_cfg

        def load(self):
            return app

    application = FlaskApplication()
    return application.run()


@manager.command
def runuwsgi(host='0.0.0.0', port='8080'):
    """Runs the app within uWSGI."""
    if host == 'localhost':
        host = '127.0.0.1'

    os.environ.setdefault('UWSGI_MODULE', 'some_app.wsgi')
    os.environ.setdefault('UWSGI_PROTOCOL', 'uwsgi')

    os.environ.setdefault('UWSGI_HTTP_SOCKET', ':%s' % port)
    os.environ.setdefault('UWSGI_HOST', host)
    os.environ.setdefault('UWSGI_PORT', port)

    os.environ.setdefault('UWSGI_MASTER', 'true')

    os.execvp('uwsgi', ('uwsgi',))


if __name__ == '__main__':
    manager.run()
