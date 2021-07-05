from django.db import models

# Create your models here.
class FileUpload(models.Model):
    ids=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    files=models.FileField(upload_to='')
    def __str__(self):
        return self.name
