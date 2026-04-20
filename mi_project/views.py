from django.http import HttpResponse

def home(request):
    return HttpResponse("""
        <h1 style="color: blue; text-align: center;">🚚 BIENVENIDO A MI PROYECTO DE ENCOMIENDAS</h1>
        <p style="text-align: center;">El sistema de gestión está listo y funcionando.</p>
    """)
