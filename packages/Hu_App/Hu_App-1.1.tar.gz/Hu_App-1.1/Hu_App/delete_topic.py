# !/usr/bin/python3

from confluent_kafka.admin import AdminClient
import yaml

def delete_topics(a, topics):
    fs = a.delete_topics(topics, operation_timeout=30)

    for topic, f in fs.items():
        try:
            f.result()
            print('Topic {} deleted'.format(topic))
        except Exception as e:
            print('Failed to delete topic {}: {}'.format(topic, e))


if __name__ == '__main__':
    file = open('./topics.yaml','r',encoding='utf-8')
    file_data = file.read()
    file.close()

    dict_data = yaml.safe_load(file_data)

    a = AdminClient({'bootstrap.servers': dict_data['kafka_addr']})

    delete_topics(a, dict_data['topics'])
