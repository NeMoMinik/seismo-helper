# syntax=docker/dockerfile:1

FROM python:3.10-slim

WORKDIR /seismo_helper

COPY requirments.txt .
RUN pip3 install -r requirments.txt

COPY . .
