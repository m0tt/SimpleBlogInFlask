FROM python:3-slim
RUN apt-get update && apt-get install -y python3-pip python-dev git && pip3 install virtualenv
RUN git clone https://github.com/m0tt/SimpleBlogInFlask.git
ENV APP_HOME ./SimpleBlogInFlask
WORKDIR $APP_HOME
RUN virtualenv -p python3 venv
RUN . venv/bin/activate && pip3 install -r requirements.txt && flask db upgrade
ENTRYPOINT . venv/bin/activate && flask run
