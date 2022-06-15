from django.db import models

# Create your models here.

class CreateWikidata(models.Model):
    tenureOrEmeritus = models.CharField(max_length=1)
    sourceFile = models.FileField(default='/User/')

    def __str__(self):
        return str(self.sourceFile)
