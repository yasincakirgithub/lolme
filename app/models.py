from django.db import models

# Create your models here.


class RiotApiKey(models.Model):
    key = models.CharField(max_length=200,null=True,blank=True)
