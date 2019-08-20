# nodejs image
FROM node:12.6.0

ADD package.json /tmp/package.json
RUN cd /tmp && npm install && npm install -g react-scripts
RUN mkdir -p /opt/reactapp && cp -a /tmp/node_modules /opt/reactapp/

WORKDIR /opt/reactapp

ADD . /opt/reactapp

# start the react app
CMD npm start

# port needed to expose - where the prod server should point to
EXPOSE 3000