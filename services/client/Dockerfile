# pull official base image
FROM node:13.5.0-alpine



# set working directory
WORKDIR /usr/src/app

# add `/usr/src/app/node_modules/.bin` to PATH
ENV PATH /usr/src/app/node_modules/.bin:$PATH

# install and cache app dependencies
COPY package.json /usr/src/app/package.json
COPY package-lock.json /usr/src/app/package-lock.json
RUN apk update && apk --no-cache add --virtual native-deps \
  g++ gcc libgcc libstdc++ linux-headers make python && \
  npm install --quiet node-gyp -g &&\
  npm ci --quiet && \
  npm install react-scripts@3.3.0 -g --silent && \
  apk del native-deps

# start app
CMD ["npm", "start"]
