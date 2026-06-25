import os
import threading
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

from django.conf import settings
from mainapp.models import SensorData
import paho.mqtt.client as mqtt

MQTT_TOPICS = [
    ('sensors/temperature', 0),
    ('sensors/humidity', 0),
    ('sensors/light', 0),
]


def save_sensor_reading(sensor_type, value, timestamp=None):
    if timestamp is None:
        timestamp = timezone.now()

    SensorData.objects.filter(sensor_type=sensor_type, is_latest=True).update(is_latest=False)
    SensorData.objects.create(
        sensor_type=sensor_type,
        value=value,
        timestamp=timestamp,
        is_latest=True,
    )


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('MQTT connected successfully')
        client.subscribe(MQTT_TOPICS)
    else:
        print('MQTT connection failed with code', rc)


def on_message(client, userdata, msg):
    try:
        value = float(msg.payload.decode('utf-8'))
        topic = msg.topic

        if topic.endswith('temperature'):
            sensor_type = SensorData.TEMPERATURE
        elif topic.endswith('humidity'):
            sensor_type = SensorData.HUMIDITY
        elif topic.endswith('light'):
            sensor_type = SensorData.LIGHT
        else:
            return

        save_sensor_reading(sensor_type, value)
    except Exception as exc:
        print('MQTT message error:', exc)


def start_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    broker_host = settings.MQTT_HOST
    broker_port = settings.MQTT_PORT

    def run():
        try:
            client.connect(broker_host, broker_port, 60)
            client.loop_forever()
        except Exception as exc:
            print('MQTT connection failed:', exc)

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
