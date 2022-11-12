from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class Lista(models.Model):
    namn=models.CharField(max_length=100)
    datum_skapad=models.DateTimeField(default=timezone.now)
    forfattare=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.namn

    def get_absolute_url(self):
        return reverse('lista-sida', kwargs={'pk':self.pk})

class Artikel(models.Model):
    namn=models.CharField(max_length=100)
    antal=models.IntegerField()
    lista=models.ForeignKey(Lista, on_delete=models.CASCADE)

    def __str__(self):
        return self.namn

    def get_absolute_url(self):
        return reverse('lista-sida', kwargs={'pk':self.lista.id})