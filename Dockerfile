# syntax=docker/dockerfile:1

FROM python:3.10-slim

WORKDIR /app

COPY requirments.txt .
RUN pip3 install -r requirments.txt

COPY . .

CMD ["python3" , "manage.py", "runserver"]