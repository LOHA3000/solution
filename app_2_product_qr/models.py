from django.db import models

class QR(models.Model):
    uuid = models.TextField()
    head_product = models.IntegerField()
    variation = models.IntegerField()
    base64 = models.TextField()
