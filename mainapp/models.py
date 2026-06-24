from django.db import models

class SensorData(models.Model):
    TEMPERATURE = 'temperature'
    HUMIDITY = 'humidity'
    LIGHT = 'light'

    SENSOR_CHOICES = [
        (TEMPERATURE, 'Temperature'),
        (HUMIDITY, 'Humidity'),
        (LIGHT, 'Light'),
    ]

    sensor_type = models.CharField(max_length=32, choices=SENSOR_CHOICES)
    value = models.FloatField()
    timestamp = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_latest = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['sensor_type', 'is_latest']),
            models.Index(fields=['timestamp']),
        ]
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.sensor_type} {self.value} @ {self.timestamp}"
