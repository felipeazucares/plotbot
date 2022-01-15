FROM node:16
WORKDIR /code/
# copy all the code across
COPY . /code
# copy across the docker version of the .env file  so we connect to containerised redis 
EXPOSE 3000
RUN npm install
CMD ["npm","start"]