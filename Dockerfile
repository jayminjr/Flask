FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["sh", "-c", "flask db upgrade && flask run --host=0.0.0.0"]