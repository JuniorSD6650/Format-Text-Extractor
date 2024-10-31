from django.db import models

class Documento(models.Model):
    titulo = models.CharField(max_length=100)
    archivo = models.FileField(upload_to='documentos/', null=True, blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

    def es_imagen(self):
        return self.archivo.name.endswith(('.png', '.jpg', '.jpeg'))

    def es_pdf(self):
        return self.archivo.name.endswith('.pdf')