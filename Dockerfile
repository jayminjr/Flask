FROM python:3.9-alpine

WORKDIR /app

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

ENV FLASK_APP=app.py

EXPOSE 5000

CMD ["sh", "-c", "flask db upgrade && flask run --host=0.0.0.0"]