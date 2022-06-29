FROM node

USER node

RUN mkdir /home/node/ssl
COPY --chown=node:node ssl/ home/node/ssl

WORKDIR home/node/client

COPY --chown=node:node client/package-lock.json client/package.json ./

RUN npm ci

COPY --chown=node:node ./client .

RUN npm run build

CMD ["npm", "start"]

