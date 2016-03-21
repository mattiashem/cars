FROM python:3
MAINTAINER Fareoffice



LABEL name="Hackathon"
LABEL vendor="Base"

RUN pip install flask
ADD code /code
RUN chmod 777 -R /code

CMD python /code/run.py

