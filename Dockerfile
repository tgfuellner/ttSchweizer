FROM ubuntu:20.04
ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
LABEL Thomas Gfuellner "thomas.gfuellner@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev build-essential
RUN apt-get install -y python3-lxml libxml2-utils
RUN apt-get install -y libffi-dev libxml2-dev libxslt-dev libpango1.0-0 libcairo2
RUN apt-get install -y libpangocairo-1.0-0
COPY . /app
WORKDIR /app/Data
# RUN pip3 install --upgrade pip
RUN pip3 install -r ../requirements.txt
ENTRYPOINT ["python3"]
CMD ["../ttSchweizerHttp.py"]
