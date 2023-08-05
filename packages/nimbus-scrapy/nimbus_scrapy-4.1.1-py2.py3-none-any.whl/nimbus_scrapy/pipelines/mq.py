# -*- coding: utf-8 -*-
import json
import logging
from scrapy.exceptions import NotConfigured, IgnoreRequest
from scrapy.utils.serialize import ScrapyJSONEncoder


class RabbitMQItemPublisherPipeline(object):
    def __init__(self, enabled, host="127.0.0.1", port=5672, user="guest", password="guest",
                 virtual_host="/", exchange="scrapy", routing_key="item", queue="item"):
        if not enabled:
            raise NotConfigured
        try:
            import pika
            self.host = host
            self.port = port
            self.user = user
            self.password = password
            self.virtual_host = virtual_host
            credentials = pika.PlainCredentials(self.user, self.password)
            parameters = pika.ConnectionParameters(self.host,
                                                   self.port,
                                                   self.virtual_host,
                                                   credentials)
            self.connection = pika.BlockingConnection(parameters=parameters)
            self.channel = self.connection.channel()
            self.exchange = exchange
            self.routing_key = routing_key
            self.queue = queue
            self.channel.exchange_declare(exchange=exchange,
                                          exchange_type="direct",
                                          durable=True)
            self.channel.queue_declare(queue=queue,
                                       durable=True)
            self.channel.queue_bind(exchange=exchange,
                                    routing_key=routing_key,
                                    queue=queue)
            self.encoder = ScrapyJSONEncoder()
        except Exception as e:
            raise NotConfigured

    @classmethod
    def from_crawler(cls, crawler):
        enabled = crawler.settings.get("ITEM_RABBIT_MQ_ENABLED")
        config = crawler.settings.get("ITEM_RABBIT_MQ")
        config = {} if config is None else config
        return cls(enabled, **config),

    def close_spider(self, spider):
        try:
            self.channel.close()
            self.connection.close()
        except Exception as e:
            pass

    def process_item(self, item, spider):
        try:
            data = self.encoder.encode(item)
            self.channel.basic_publish(
                exchange=self.exchange,
                routing_key=self.routing_key,
                body=data,
            )
        except Exception as e:
            spider.log(e, level=logging.ERROR)
            spider.log(item, level=logging.INFO)
        return item
