from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from django.contrib import messages 
from django.utils import timezone 

from .models import Encomienda, Empleado
from mi_project.choices import EstadoEnvio
from django.core.paginator import Paginator
from django.db.models import Q

# ── Vista mínima ────────────────────────────────────────────── 
def mi_vista(request): 
    # 1. Recibe el request 
    # 2. Ejecuta lógica 
    # 3. Devuelve una respuesta 
    from django.http import HttpResponse 
    return HttpResponse('Hola desde Django')


# ── Vista real: dashboard del sistema ──────────────────────── 
@login_required 
def dashboard(request): 
    """Vista principal del sistema con estadísticas""" 
    hoy = timezone.now().date() 
    context = { 
    'total_activas':   Encomienda.objects.activas().count(), 
    'en_transito':     Encomienda.objects.en_transito().count(),    
    'con_retraso':0 ,  #Encomienda:  objects.con_retraso().count(),     
    'entregadas_hoy':  Encomienda.objects.filter( 
                            estado=EstadoEnvio.ENTREGADO, 
                            fecha_entrega_real=hoy).count(), 
    'ultimas':         Encomienda.objects.con_relaciones()[:5], 
    }
    return render(request, 'envios/dashboard.html', context)


@login_required
def encomienda_crear(request):
    """
    GET  → muestra el formulario vacío
    POST → valida, guarda y redirige al detalle
    """

    from .forms import EncomiendaForm

    if request.method == 'POST':

        form = EncomiendaForm(request.POST)

        if form.is_valid():

            enc = form.save(commit=False)   # no guarda aún en BD

            enc.empleado_registro = Empleado.objects.get(
                email=request.user.email
            )

            enc.save()   # ahora sí guarda

            messages.success(
                request,
                f'Encomienda {enc.codigo} registrada correctamente.'
            )

            # Redirige para evitar reenvío del formulario al recargar

            return redirect('encomienda_detalle', pk=enc.pk)

        # Si el form tiene errores, vuelve a mostrar con los errores

    else:

        form = EncomiendaForm()

    # GET: form vacío

    return render(request, 'envios/form.html', {
        'form': form,
        'titulo': 'Nueva Encomienda',
    })


@login_required
def encomienda_lista(request):

    qs = Encomienda.objects.con_relaciones()

    # ── Filtros opcionales ────────────────────────────────────────

    estado = request.GET.get('estado', '')
    q = request.GET.get('q', '')

    if estado:
        qs = qs.filter(estado=estado)

    if q:
        qs = qs.filter(
            Q(codigo__icontains=q) |
            Q(remitente__apellidos__icontains=q) |
            Q(destinatario__apellidos__icontains=q)
        )

    # ── Paginación ────────────────────────────────────────────────

    paginator = Paginator(qs, 15)

    page_number = request.GET.get('page', 1)

    encomiendas = paginator.get_page(page_number)

    return render(request, 'envios/lista.html', {
        'encomiendas': encomiendas,
        'estados': EstadoEnvio.choices,
        'estado_activo': estado,
        'q': q,
    })