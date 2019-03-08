from django.db import models


# Create your models here.
class Image(models.Model):

    name = models.CharField(max_length=100)
    location = models.CharField(max_length=13)
    size = models.CharField(max_length=9)
    url = models.CharField(max_length=100)
    picture = models.ImageField(default='jeep.png', blank=True)

    def __str__(self):
        return self.name.__str__() + "-" + self.size.__str__()
