import random
import string

from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=15, unique=True)
    user_invite_code = models.CharField(max_length=6, blank=True, null=True)
    activate_invite_code = models.CharField(max_length=6, blank=True, null=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.user_invite_code:
            self.user_invite_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        super().save(*args, **kwargs)

    def get_who_activate_my_code(self):
        res = []
        for user in User.objects.filter(activate_invite_code=self.user_invite_code):
            res.append(user.phone_number)
        return res
