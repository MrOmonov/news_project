from django.db import models


class Publishedmanager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='PB')
