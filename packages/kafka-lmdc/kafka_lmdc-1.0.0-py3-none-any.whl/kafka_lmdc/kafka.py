import os
import json
import sys
from confluent_kafka import Producer, Consumer, KafkaError


# Biblioteca para Python & Kafka
# Read: https://docs.confluent.io/current/installation/configuration/consumer-configs.html

class kafkaAPI():

    @staticmethod
    def createConsumerWithKerberos(kafka_ip: str, group_id: str, kerberosKeyTabPath: str, kerberosUsername: str,
                                   autoOffsetReset: str='earliest', securityProtocol: str='SASL_PLAINTEXT'):
        conf = {
            'bootstrap.servers': kafka_ip,
            'group.id': group_id,
            'auto.offset.reset': autoOffsetReset,
            'security.protocol': securityProtocol,
            'sasl.mechanism': 'GSSAPI',
            'sasl.kerberos.service.name': 'kafka',
            'sasl.kerberos.keytab': kerberosKeyTabPath,
            'sasl.kerberos.principal': kerberosUsername
        }

        c = Consumer(conf)
        return c

    @staticmethod
    def createConsumerWithLoginAndPass(kafka_ip: str, group_id: str, kafkaUserName: str, kafkaPassword: str,
                                       autoOffsetReset: str='earliest', securityProtocol: str='SASL_PLAINTEXT'):

        conf = {'bootstrap.servers': kafka_ip,
                'group.id': group_id,
                'auto.offset.reset': autoOffsetReset,
                'security.protocol': securityProtocol,
                'sasl.mechanism': 'PLAIN',
                'sasl.username':kafkaUserName,
                'sasl.password': kafkaPassword
        }

        c = Consumer(conf)
        return c

    @staticmethod
    def createConsumerWithoutLogin(kafka_ip: str, group_id: str, autoOffsetReset: str='earliest'):
        conf = {
            'bootstrap.servers': kafka_ip,
            'group.id': group_id,
            'auto.offset.reset': autoOffsetReset
        }

        c = Consumer(conf)
        return c

    @staticmethod
    def createProducerWithKerberos(kafka_ip: str, kafka_krb5_user_keytab_path: str, kafka_krb5_username: str,
                                   securityProtocol: str='SASL_PLAINTEXT', kafka_debug: bool=False):
        producer_conf = {'bootstrap.servers': kafka_ip,
                         'security.protocol': securityProtocol,
                         'sasl.mechanism': 'GSSAPI',
                         'sasl.kerberos.service.name': 'kafka',
                         'sasl.kerberos.keytab': kafka_krb5_user_keytab_path,
                         'sasl.kerberos.principal': kafka_krb5_username}

        try:
            if kafka_debug:
                producer_conf['debug'] = 'security,broker'
            producer = Producer(**producer_conf)
            return producer
        except BufferError:
            sys.stderr.write('%% Local producer queue is full (%d messages awaiting delivery): try again\n' % len(producer))
            return None

    @staticmethod
    def createProducerWithLoginAndPass(kafka_ip: str, kafkaUserName: str, kafkaPassword: str,
                                       securityProtocol: str='SASL_PLAINTEXT', kafka_debug: bool=False):
        # check this function
        try:
            producer_conf = {'bootstrap.servers': kafka_ip,
                            'security.protocol': securityProtocol,
                            'sasl.mechanism': 'PLAIN',
                            'sasl.username':kafkaUserName,
                            'sasl.password': kafkaPassword}
            if kafka_debug:
                producer_conf['debug'] = 'security,broker'

            producer = Producer(**producer_conf)
            return producer

        except BufferError:
            sys.stderr.write('%% Local producer queue is full (%d messages awaiting delivery): try again\n' % len(producer))
            return None

    @staticmethod
    def createProducerWithoutLogin(kafka_ip: str, kafka_debug: bool=False):
        try:
            producer_conf = {'bootstrap.servers': kafka_ip}
            if kafka_debug:
                producer_conf['debug'] = 'security,broker'

            producer = Producer(**producer_conf)
            return producer

        except BufferError:
            sys.stderr.write('%% Local producer queue is full (%d messages awaiting delivery): try again\n' % len(producer))
            return None