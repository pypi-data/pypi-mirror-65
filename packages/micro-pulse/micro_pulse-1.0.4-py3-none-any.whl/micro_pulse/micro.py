from kafka import KafkaConsumer
from kafka import KafkaProducer
import json
import logging

class Micro():
  consumer = None
  producer = None
  topics = None
  pattern = None
  logger = None

  def __init__(self, options=None):
    self.logger = logging.getLogger('micro-pulse')
    self.logger.addHandler(logging.StreamHandler())
    self.logger.setLevel(logging.DEBUG)
    # options = self.setup(options)
    pass

  def deserialize(self, v):
    try:
      data = json.loads(v.decode('utf-8'))
    except Exception as e:
      self.logger.error(f'Deserialize error : {e}')
      self.logger.info(v)
    return data

  def serialize(self, v):
    try:
      data = json.dumps(v).encode('utf-8')
    except Exception as e:
      self.logger.error(f'Serialize error : {e}')
    return data

  def setup(self, options):
    self.consumer = KafkaConsumer(
      bootstrap_servers=options['bootstrap_servers'],
      group_id=options['group_id'],
      value_deserializer=self.deserialize,
      enable_auto_commit=options['enable_auto_commit'],
      auto_offset_reset=options['auto_offset_reset'],
      auto_commit_interval_ms=options['auto_commit_interval_ms'],
      consumer_timeout_ms=options['consumer_timeout_ms']
    )

    self.producer = KafkaProducer(
      bootstrap_servers='161.35.16.43:32033',
      value_serializer=self.serialize
    )

    return options

  def subscribe(self, topic=None, topics=None, pattern=None):
    if topic:
      return self.consumer.subscribe(topic)

    if topics:
      return self.consumer.subscribe(topics=topics)

    if pattern:
      return self.consumer.subscribe(pattern=pattern)

  def run(self, callback=None):
    data = {}
    response = None

    while True:
      for msg in self.consumer:
        if not callback:
          self.logger.info('Using default process function')
          self.process(msg)
        else:
          if callable(callback):
            self.logger.info(f'Processing msg {msg.offset} from {msg.topic}')
            new_data = callback(msg, service=self)

      #endfor
    #endwhile
    #pass

  def process(self, data):
    pass
