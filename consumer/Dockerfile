FROM python:3.7-buster
USER root

RUN pip install kafka-python==2.0.2 \
    flair==0.11.1

WORKDIR /usr/src/app

COPY consumer/start_consumer.py ./
COPY producer/topics.txt ./

VOLUME ["/root/.flair"]

ENTRYPOINT [ "python" ]
CMD [ "start_consumer.py" ]
