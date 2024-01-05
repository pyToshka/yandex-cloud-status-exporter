ARG PYTHON_IMAGE=gcr.io/distroless/python3:nonroot
FROM python:3.9-slim AS build-env
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
COPY app.py /app/
COPY wsgi.py /app/
COPY requirements.txt /app
WORKDIR /app

RUN pip install --no-cache-dir --upgrade -r requirements.txt  \
    &&  cp "$(which uwsgi)" /app && rm -rf requirements.txt

FROM $PYTHON_IMAGE
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONPATH=/usr/local/lib/python3.9/site-packages
COPY --from=build-env /app /app
COPY --from=build-env /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
WORKDIR /app
EXPOSE 5000
CMD [ "uwsgi", "--http", "0.0.0.0:5000", "-p", "4", "-w", "wsgi:app"]
