from django.shortcuts import render, get_object_or_404
from django.http import FileResponse
from .models import Documento
from .forms import DocumentoForm 
import fitz  # PyMuPDF
import io

# Definimos constantes para las coordenadas y colores de los cuadros
RECTANGLES = {
    "rojo": {"rect": fitz.Rect(30, 50, 550, 110), "color": (1, 0, 0)},
    "verde": {"rect": fitz.Rect(90, 150, 245, 650), "color": (0, 1, 0)},
}

def cargar_documento(request):
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            documento = form.save()
            return render(request, 'app/resultado.html', {'documento': documento})

    else:
        form = DocumentoForm()

    return render(request, 'app/cargar.html', {'form': form})

def extraer_texto(request, documento_id):
    documento = get_object_or_404(Documento, id=documento_id)

    # Lista de claves que queremos encontrar en el cuadro rojo
    claves_rojo = [
        "CÓDIGO", "CICLO", "SEMESTRE", "CREDITOS PERMITIDOS", 
        "SEDE", "CREDITO TOTAL", "PLAN", "CREDITOS ADICIONALES"
    ]
    
    texto_cuadro_rojo = []
    texto_cuadro_verde = []

    if documento.es_pdf():
        pdf_path = documento.archivo.path
        pdf = fitz.open(pdf_path)
        pagina = pdf[0]

        # Extraer y organizar el texto del cuadro rojo
        raw_text_rojo = pagina.get_text("text", clip=RECTANGLES["rojo"]["rect"])
        for clave in claves_rojo:
            start_index = raw_text_rojo.find(clave)
            if start_index != -1:
                end_index = len(raw_text_rojo)
                for next_clave in claves_rojo:
                    next_index = raw_text_rojo.find(next_clave, start_index + 1)
                    if next_index != -1:
                        end_index = min(end_index, next_index)
                valor = raw_text_rojo[start_index + len(clave) + 1:end_index].strip()
                texto_cuadro_rojo.append({"etiqueta": clave, "valor": valor})

        # Extraer y formatear el texto dentro del segundo cuadro (verde)
        raw_text_verde = pagina.get_text("text", clip=RECTANGLES["verde"]["rect"])
        cursos = raw_text_verde.split("-")  # Separar cada curso con su docente
        for curso in cursos:
            curso_info = curso.strip()
            if curso_info:
                texto_cuadro_verde.append(curso_info)

        pdf.close()

    return render(request, 'app/resultado.html', {
        'documento': documento,
        'texto_cuadro_rojo': texto_cuadro_rojo,
        'texto_cuadro_verde': texto_cuadro_verde,
    })

def ver_documento(request, documento_id):
    # Obtener el documento de la base de datos
    documento = get_object_or_404(Documento, id=documento_id)
    
    if documento.es_pdf():
        # Abre el PDF sin modificar el archivo original
        pdf_path = documento.archivo.path
        pdf = fitz.open(pdf_path)
        pagina = pdf[0]  # Seleccionamos la primera página

        # Dibujar los rectángulos temporalmente
        for color_key, info in RECTANGLES.items():
            pagina.draw_rect(info["rect"], color=info["color"], width=1)

        # Guardar el PDF temporal en memoria
        pdf_io = io.BytesIO()
        pdf.save(pdf_io)
        pdf.close()
        pdf_io.seek(0)

        # Devolver el PDF con los cuadros como respuesta
        return FileResponse(pdf_io, as_attachment=False, content_type='application/pdf')
    
    # Si no es un PDF, mostrar una página de error o redirigir
    return render(request, 'app/error.html', {'mensaje': 'El archivo no es un PDF válido.'})

def resultado_documento(request, documento_id):
    # Obtener el documento de la base de datos
    documento = get_object_or_404(Documento, id=documento_id)
    
    return render(request, 'app/resultado.html', {'documento': documento})
