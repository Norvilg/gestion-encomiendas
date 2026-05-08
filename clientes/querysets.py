from django.db import models

class ClienteQuerySet(models.QuerySet):

    def activos(self):
        return self.filter(estado=1)

    def de_baja(self):
        return self.filter(estado=9)