FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /sources
WORKDIR /sources
ADD sdaquiz /sources/
RUN pip install -r requirements.txt
EXPOSE 7000
CMD exec gunicorn sdaquiz.wsgi:application -w 3 -b 0.0.0.0:7000
