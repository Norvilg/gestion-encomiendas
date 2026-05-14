from django.urls import path
from . import views
from . import views_cbv

urlpatterns = [

    # Dashboard principal
    path(
        '',
        views.dashboard,
        name='dashboard'
    ),

    # Lista de encomiendas
    path(
        'encomiendas/',
        views_cbv.EncomiendaListView.as_view(),
        name='encomienda_lista'
    ),

    # Crear nueva encomienda
    path(
        'encomiendas/nueva/',
        views_cbv.EncomiendaCreateView.as_view(),
        name='encomienda_crear'
    ),

    # Detalle
    path(
        'encomiendas/<int:pk>/',
        views_cbv.EncomiendaDetailView.as_view(),
        name='encomienda_detalle'
    ),

    # Editar
    path(
        'encomiendas/<int:pk>/editar/',
        views_cbv.EncomiendaUpdateView.as_view(),
        name='encomienda_editar'
    ),
]