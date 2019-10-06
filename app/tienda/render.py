from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa

"""
Todos los archivos render.py son los encargados de crear los pdf
esta liberia xhtml2pdf lo que hace es pasar un html a pdf, cabe aclarar
que esta liberia no soporta inserciones de codigo js y cuenta con pocos
estilos, para mas información consultar la documentacion.

"""

class RenderPdf:

    @staticmethod
    def render(path: str, params: dict):
        template = get_template(path)
        html = template.render(params)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
        if not pdf.err:
            response = HttpResponse(response.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename=reporte.pdf'
            return  response
            
        else:
            return HttpResponse("Error Rendering PDF", status=400)
