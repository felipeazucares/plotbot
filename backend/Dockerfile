FROM python:3.9.9-slim as builder
RUN python3 -m venv /py3
WORKDIR /code/
COPY requirements.txt /code/requirements.txt
RUN /py3/bin/pip install --no-cache-dir --upgrade -r /code/requirements.txt
# copy all the code across
COPY . /code

EXPOSE 8450
CMD ["/py3/bin/python3", "main.py"]