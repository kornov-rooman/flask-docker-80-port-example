import os
import grp
import pwd

_uid = os.getuid()
_user_name = pwd.getpwuid(_uid).pw_name
_group_name = grp.getgrgid(_uid).gr_name

bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:8080')
workers = os.environ.get('GUNICORN_WORKERS', 4)

reload = True
preload_app = True
raw_env = [
    'LANG=ru_RU.UTF-8',
    'LC_ALL=ru_RU.UTF-8',
    'LC_LANG=ru_RU.UTF-8'
]

timeout = os.environ.get('GUNICORN_TIMEOUT', 10)

user = _user_name
group = _group_name

accesslog = '-'
errorlog = '-'
