FROM ubuntu:16.04
MAINTAINER Thomas Gfuellner "thomas.gfuellner@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev build-essential
RUN apt-get install -y python3-lxml libxml2-utils
RUN apt-get install -y libffi-dev libxml2-dev libxslt-dev libpango1.0-0 libcairo2
COPY . /app
WORKDIR /app/Daten
RUN pip3 install -r ../requirements.txt
ENTRYPOINT ["python3"]
CMD ["../ttSchweizerHttp.py"]
