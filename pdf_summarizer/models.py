from django.db import models

# Create your models here.
from django.db import models

from django.db import models

class PDFDocument(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

