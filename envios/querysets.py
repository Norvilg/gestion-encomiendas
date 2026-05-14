from django.db import models

class EncomiendaQuerySet(models.QuerySet):

    def pendientes(self):
        return self.filter(estado='PE')

    def en_transito(self):
        return self.filter(estado='TR')

    def entregadas(self):
        return self.filter(estado='EN')

    def devueltas(self):
        return self.filter(estado='DV')

    def activas(self):
        return self.filter(estado__in=['PE', 'TR', 'DE'])

    def con_relaciones(self):
        return self.select_related(
            'remitente',
            'destinatario',
            'ruta',
            'empleado'
        )