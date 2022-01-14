FROM python:3.9
WORKDIR /code/
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
# copy all the code across
COPY . /code
# copy across the docker version of the .env file  so we connect to containerised redis 
# COPY ./server/.env_docker /code/.env
EXPOSE 9000
CMD ["python", "main.py"]