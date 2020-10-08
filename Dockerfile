# python version image
FROM python:3.7

# Environment variables
ENV PYTHONUNBUFFERED = 1


# Work directory
WORKDIR /src
COPY requirements.txt /src/
RUN pip install -r requirements.txt
COPY . /src/
