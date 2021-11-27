from django.db import models


class File(models.Model):
    name = models.FileField(blank=True, )

    def __str__(self):
        return str(self.name)
