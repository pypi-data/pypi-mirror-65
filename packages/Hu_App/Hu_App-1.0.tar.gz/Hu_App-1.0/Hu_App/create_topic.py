# ！/usr/bin/python

from confluent_kafka.admin import AdminClient, NewTopic
import yaml

file = open('./topics.yaml', 'r', encoding='utf-8')
file_data = file.read()
file.close()

dict_data = yaml.safe_load(file_data)

new_topics = [NewTopic(topic, num_partitions=1, replication_factor=2) for topic in dict_data['topics']]

a = AdminClient({'bootstrap.servers': dict_data['kafka_addr']})
fs = a.create_topics(new_topics)

for topic, f in fs.items():
    try:
        f.result()
        print('Topic {} created'.format(topic))
    except Exception as e:
        print('Failed to create topic {}: {}'.format(topic, e))
