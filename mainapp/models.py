from django.db import models
class SensorData(models.Model):
    device_name = models.CharField(max_length=50)
    temperature = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.device_name