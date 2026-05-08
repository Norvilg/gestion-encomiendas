from django.db import models

class EstadoGeneral(models.TextChoices):
    ACTIVO = 'Activo', 'Activo'
    INACTIVO = 'Inactivo', 'Inactivo'

class EstadoEnvio(models.TextChoices):
    PENDIENTE = 'PE', 'Pendiente'
    EN_TRANSITO = 'TR', 'En tránsito' 
    EN_DESTINO = 'DE', 'En destino' 
    ENTREGADO = 'EN', 'Entregado' 
    DEVUELTO = 'DV', 'Devuelto' 

class TipoDocumento(models.TextChoices):
    DNI = 'DNI', 'DNI'
    RUC = 'RUC', 'RUC'
    PASAPORTE = 'PAS', 'Pasaporte'