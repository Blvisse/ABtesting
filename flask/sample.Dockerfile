FROM python:3.7-slim-buster


COPY ../requirements.txt /requirements.txt 

RUN pip install -r requirements.txt 

ADD . /flask

WORKDIR  /flask

EXPOSE 8000

# CMD ["flask"."run","--host=0.0.0.0","--port=8000"]


CMD python app.py


