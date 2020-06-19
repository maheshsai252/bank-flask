FROM python:3.7
ADD . /bank
WORKDIR /bank
RUN pip install -r requirements.txt
