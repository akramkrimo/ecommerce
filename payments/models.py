from django.db import models

from accounts.models import User

# Create your models here.


class Card(models.Model):
    brand = models.CharField(max_length=20)
    last_4 = models.IntegerField()
    fingerprint = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    user  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')

    def __str__(self):
        return self.brand + ': ' + str(self.last_4)

