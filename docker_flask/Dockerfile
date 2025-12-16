# official python image
FROM python:3.10-slim

# working dir
WORKDIR /app

COPY . /app

RUN pip install flask

EXPOSE 5000

CMD ["python", "app.py"]