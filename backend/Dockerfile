FROM python:3.9
WORKDIR /app
RUN pip install gunicorn==20.1.0
COPY ./backend/requirements.txt .
RUN pip install -r requirements.txt --no-deps --no-cache-dir
COPY ./backend .
COPY ./data/ ../data
COPY ./docs ../docs/
ENTRYPOINT ["sh", "/app/entrypoint.sh" ]