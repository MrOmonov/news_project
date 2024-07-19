from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='users/images', null=True, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} profili"

    def get_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"