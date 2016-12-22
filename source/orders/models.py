from django.conf import settings
from django.db import models


class UserCheckout(models.Model):
    user = models.OneToOneField(
            settings.AUTH_USER_MODEL,
            null=True,
            blank=True
            )
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email
