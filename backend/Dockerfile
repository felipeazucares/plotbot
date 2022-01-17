FROM python:3.9.9-slim as builder
RUN python3 -m venv /py3
WORKDIR /code/
COPY requirements.txt /code/requirements.txt
RUN /py3/bin/pip install --no-cache-dir --upgrade -r /code/requirements.txt
# copy all the code across
COPY . /code
# copy across the docker version of the .env file  so we connect to containerised redis 
# COPY ./server/.env_docker /code/.env

FROM python:3.9.9-slim
# copy across the virtual build
COPY --from=builder /py3 /py3
COPY --from=builder /code/ .
EXPOSE 8450
CMD ["/py3/bin/python3", "main.py"]