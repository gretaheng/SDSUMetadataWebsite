from django.db import models

# Create your models here.

class DataPrep(models.Model):
    fieldQnum = models.CharField(max_length=20)
    departmentQnum = models.CharField(max_length=20)
    websiteBaseUrl = models.CharField(max_length=100)
    allOnePage = models.BooleanField(default=False)
    file = models.FileField(default='/User/')

    def __str__(self):
        return self.departmentQnum
