FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /olx_clone
WORKDIR /olx_clone
ADD . /olx_clone/
RUN pip install -r requirements.txt