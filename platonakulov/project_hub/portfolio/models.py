from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string

class Fuel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo_url = models.URLField(blank=True)
    slug = models.SlugField(max_length=12, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        random_slug = get_random_string(length=12)
        return random_slug

    def __str__(self):
        return self.name



class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fuel_slug = models.SlugField(max_length=12)  # Ссылка на уникальный URL топлива

    def __str__(self):
        return f"{self.user.username}'s Cart Item - {self.fuel_slug}"

class Review(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
