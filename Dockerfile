FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -vvv -r requirements.txt

EXPOSE 5000

ENV NAME World

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]