FROM node:20.11-slim

WORKDIR /app
COPY package*.json .

RUN npm ci --loglevel verbose

COPY . .

CMD [ "npm", "start" ]