from django.urls import path
from app.tienda import views
app_name = 'tienda'

urlpatterns = [
    path('',views.login, name='login'),
    path('admin_nuevo_o_que/',views.nuevoAdmin),
    path('menu/',views.menu, name='menu'),
    path('tabla/<str:tipo>/',views.VistaFactory,name='tabla'),
    path('autocompletar/<str:tipo>/',views.CompletarFactory),
    path('editar/<str:tipo>/',views.EditarFactory),
    path('eliminar/<str:tipo>/',views.EliminarFactory),
    path('insertar/<str:tipo>/',views.AgregarFactory),
    path('csv/<str:tipo>/',views.CsvFactory),
    path('pdf/<str:tipo>/',views.PdfFactory),
    path('deslogear/',views.deslogear,name='deslogear'),
]