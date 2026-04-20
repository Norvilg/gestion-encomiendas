from django.db import models

class Ruta(models.Model):
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.origen} - {self.destino}"