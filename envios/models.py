from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

from mi_project.choices import EstadoGeneral, EstadoEnvio
from .vaidators import validar_peso_positivo
from .querysets import EncomiendaQuerySet
from clientes.models import Cliente
from rutas.models import Ruta


class Empleado(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    cargo = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    estado = models.IntegerField(choices=EstadoGeneral.choices, default=EstadoGeneral.ACTIVO)
    fecha_ingreso = models.DateField()

    def __str__(self):
        return f"{self.codigo} - {self.apellidos} {self.nombres}"

    class Meta:
        db_table = 'empleados'
        ordering = ['apellidos', 'nombres']


class Encomienda(models.Model):
    
    objects = EncomiendaQuerySet.as_manager()

    codigo = models.CharField(max_length=20, unique=True)
    descripcion = models.TextField()

    peso_kg = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[validar_peso_positivo, MinValueValidator(0.01)]
    )

    costo_envio = models.DecimalField(max_digits=10, decimal_places=2)

    remitente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='enviados')
    destinatario = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='recibidos')
    ruta = models.ForeignKey(Ruta, on_delete=models.PROTECT, related_name='encomiendas')
    empleado = models.ForeignKey(Empleado, on_delete=models.PROTECT, related_name='encomiendas')

    estado = models.CharField(max_length=2, choices=EstadoEnvio.choices, default=EstadoEnvio.PENDIENTE)

    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_entrega_est = models.DateField(null=True, blank=True)
    fecha_entrega_real = models.DateField(null=True, blank=True)
    observaciones = models.TextField(blank=True, null=True)

    # ---------------- VALIDACIONES ----------------
    def clean(self):
        errors = {}

        if self.remitente_id and self.destinatario_id:
            if self.remitente_id == self.destinatario_id:
                errors['destinatario'] = 'Remitente y destinatario no pueden ser iguales.'

        if self.fecha_entrega_est and self.fecha_entrega_est < timezone.now().date():
            errors['fecha_entrega_est'] = 'No puede ser una fecha pasada.'

        if self.fecha_entrega_real and self.fecha_entrega_est:
            if self.fecha_entrega_real < self.fecha_entrega_est:
                errors['fecha_entrega_real'] = 'No puede ser menor a la estimada.'

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    # ---------------- MÉTODOS ----------------
    def cambiar_estado(self, nuevo_estado, empleado, observacion=''):

        if nuevo_estado == self.estado:
            raise ValueError(f"Ya está en estado {self.get_estado_display()}")

        estado_anterior = self.estado
        self.estado = nuevo_estado

        if nuevo_estado == EstadoEnvio.ENTREGADO:
            self.fecha_entrega_real = timezone.now().date()

        self.save()

        HistorialEstado.objects.create(
            encomienda=self,
            estado_anterior=estado_anterior,
            estado_nuevo=nuevo_estado,
            empleado=empleado,
            observacion=observacion
        )

        return self

    def calcular_costo(self):
        PRECIO_POR_KG_EXTRA = 2.50
        PESO_BASE = 5

        costo = self.ruta.precio_base

        if self.peso_kg > PESO_BASE:
            costo += (self.peso_kg - PESO_BASE) * PRECIO_POR_KG_EXTRA

        return round(costo, 2)

    # ---------------- PROPERTIES ----------------
    @property
    def esta_entregada(self):
        return self.estado == EstadoEnvio.ENTREGADO

    @property
    def dias_en_transito(self):
        return (timezone.now().date() - self.fecha_registro.date()).days

    @property
    def descripcion_corta(self):
        return self.descripcion[:50] + "..." if len(self.descripcion) > 50 else self.descripcion
    
    # Métodos @classmethod para consultas comunes
    @classmethod
    def crear_con_costo_calculado(
        cls,
        remitente,
        destinatario,
        ruta,
        empleado,
        descripcion,
        peso_kg,
        **kwargs
    ):
        import uuid
        from django.utils import timezone
        from datetime import timedelta

        codigo = f"ENC-{timezone.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:6].upper()}"

        fecha_est = timezone.now().date() + timedelta(days=ruta.dias_entrega)

        encomienda = cls(
            codigo=codigo,
            descripcion=descripcion,
            peso_kg=peso_kg,
            remitente=remitente,
            destinatario=destinatario,
            ruta=ruta,
            empleado=empleado,
            fecha_entrega_est=fecha_est,
            **kwargs
        )

        encomienda.costo_envio = encomienda.calcular_costo()
        encomienda.save()

        return encomienda


class HistorialEstado(models.Model):
    encomienda = models.ForeignKey(Encomienda, on_delete=models.CASCADE, related_name='historial')
    estado_anterior = models.CharField(max_length=2, choices=EstadoEnvio.choices)
    estado_nuevo = models.CharField(max_length=2, choices=EstadoEnvio.choices)
    observacion = models.TextField(blank=True, null=True)
    empleado = models.ForeignKey(Empleado, on_delete=models.PROTECT, related_name='cambios_estado')
    fecha_cambio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.encomienda.codigo}: {self.estado_anterior} → {self.estado_nuevo}"

    class Meta:
        db_table = 'historial_estados'
        ordering = ['-fecha_cambio']