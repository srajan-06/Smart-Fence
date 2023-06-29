from django.db import models

class DetectedImage(models.Model):
    image = models.ImageField(upload_to='media/fence/')
    timestamp = models.DateTimeField(auto_now_add=True)

