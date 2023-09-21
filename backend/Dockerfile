FROM python:3.9
WORKDIR /app
RUN pip install gunicorn==20.1.0
COPY ./backend/requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY ./backend .
COPY ./data ../data
ENTRYPOINT ["sh", "/app/entrypoint.sh" ]