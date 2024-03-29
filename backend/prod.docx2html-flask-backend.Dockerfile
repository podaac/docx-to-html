# ubuntu image so we can install inkscape and spacy
FROM ubuntu

# install python & pip
RUN apt-get update && apt-get upgrade -y && apt-get install -y python3 python3-pip python3-dev && cd /usr/local/bin && ln -s /usr/bin/python3 python && pip3 install --upgrade pip

# no interactive gui when installing packages - software-properties-common allows inkscape to install
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install software-properties-common

# install inkscape
RUN add-apt-repository universe && add-apt-repository ppa:inkscape.dev/stable && apt-get update && apt-get install inkscape -y

RUN mkdir -p /opt/backend-app 

WORKDIR /opt/backend-app
ADD . /opt/backend-app

# install pip libraries/dependencies
RUN pip3 install -r requirements.txt

# install spacy nlp library - sm for small library, if we need vectors install en_core_web_lg and change in nlp.py
RUN python3 -m spacy download en_core_web_lg

# run the app through uwsgi server and go through app.ini settings
CMD [ "uwsgi", "app.ini" ]