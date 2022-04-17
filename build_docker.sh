echo 'Build producer'
docker build -t producer-kafka -f producer/Dockerfile .

echo 'Build consumer'
docker build -t consumer-kafka -f consumer/Dockerfile .

# run normally
# docker run -it --rm --name producer-kafka -v "$PWD":/usr/src/myapp -w /usr/src/myapp python:3 python start_producers.py

# /opt/bitnami/kafka/bin/kafka-topics.sh --bootstrap-server kafka:9092 --create --replication-factor 1 --partitions 1 --topic ETH
echo 'Running'
docker-compose -f docker-compose.yml up -d

