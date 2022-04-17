FROM python:3.7-buster
USER root

RUN pip install kafka-python==2.0.2 \
		tweepy==3.10.0

WORKDIR /usr/src/app

COPY producer/start_producer.py ./
COPY producer/topics.txt ./

ENTRYPOINT [ "python" ]
CMD [ "start_producer.py" ]
