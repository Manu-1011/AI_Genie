from django.db import models

class UploadedDataset(models.Model):
    file = models.FileField(upload_to='datasets/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

class UserQuery(models.Model):
    dataset = models.ForeignKey(UploadedDataset, on_delete=models.CASCADE)
    question = models.TextField()
    response = models.TextField()
    chart = models.ImageField(upload_to='charts/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query on {self.dataset} - {self.created_at}"
