FROM python:3.10

# django_web environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# django_web work directory
WORKDIR /music/
RUN apt-get update
# Create logs directory and log files
COPY . /music/

# 添加 pip 清华镜像源
RUN pip install pip -U -i https://pypi.tuna.tsinghua.edu.cn/simple
# 添加 pip 清华镜像源
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN python manage.py makemigrations
RUN python manage.py migrate
CMD ["gunicorn", "djangoProject.wsgi:application", "-c", "gunicorn.conf.py"]

