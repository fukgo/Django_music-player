
bind = "0.0.0.0:8080"
workers = 4  # 例如，设置工作进程数
timeout = 120  # 设置超时时间
accesslog = '/music/gunicorn_log/access.log'
errorlog = '/music/gunicorn_log/error.log'
wsgi_app = 'djangoProject.wsgi:application'
loglevel = 'debug'
